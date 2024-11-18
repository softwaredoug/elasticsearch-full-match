"""Tests a full field match - defined by every query token matching every position and nothing else."""
import pytest
import json
import elasticsearch_full.shingles as shingles
import elasticsearch_full.conditional as conditional
import elasticsearch_full.keyword as keyword
import elasticsearch_full.sentinel as sentinel
from elasticsearch import Elasticsearch


class ElasticsearchFixture:

    def __init__(self, index_name, query_fn, analysis_settings, analyzer):
        self.analyzer = analyzer
        self.es = self._create_index(index_name, analysis_settings)
        self.index_name = index_name
        self.query_fn = query_fn

    def analyze(self, text):
        response = self.es.indices.analyze(
            index=self.index_name,
            body={
                "analyzer": self.analyzer,
                "text": text
            }
        )
        # print(json.dumps(response['detail'], indent=2))
        tokens = " _ ".join([token["token"] for token in response["tokens"]])
        print(f"Analyzed: {text} -> {tokens}")
        return tokens

    def _create_index(self, index, analysis_settings):
        es = Elasticsearch("http://localhost:9200")
        es.indices.delete(index=index, ignore=[400, 404])
        settings = {
            "settings": {
                "max_shingle_diff": 10,
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": analysis_settings
            },
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": self.analyzer
                    }
                }
            }
        }
        es.indices.create(index=index, body=settings)
        return es

    def index_docs(self, docs):
        for id, doc in enumerate(docs):
            self.es.index(index=self.index_name,
                          id=id,
                          body={"title": doc})
        self.es.indices.refresh(index=self.index_name)

    def search(self, keywords, profile=True):
        body = self.query_fn("title", keywords)
        if profile:
            body['profile'] = True
        response = self.es.search(index=self.index_name, body=body)
        if profile and 'profile' in response:
            took = response['took']
            print("************")
            print(f"Query: {keywords}")
            print(f"Query took {took}ms")
            print(json.dumps(response["profile"], indent=2))
        return response


TEST_DOCS = [
    "Steam Decks reviewed from a PC gamer",
    "steam deck review from a PC gamer",
    "Steam Deck review",
    "Steam Deck review steam deck Review",
    "Steam Deck",
    "Steam"
]


@pytest.fixture(scope="module", params=[conditional])  # [sentinel, shingles, conditional, keyword])
def elasticsearch_fixture(request):
    module = request.param
    index_name = module.__name__.split(".")[-1]
    analysis_settings, configured_analyzer = module.analysis()
    es = ElasticsearchFixture(query_fn=module.query, index_name=index_name, analysis_settings=analysis_settings,
                              analyzer=configured_analyzer)
    es.index_docs(TEST_DOCS)
    return es


@pytest.mark.parametrize("keywords, expected_matches",
                         [["Steam", [5]],
                          ["Steam Deck", [4]],
                          ["Steam Deck review", [2]],
                          ["Steam Deck reviews", [2]],
                          ["review", []],
                          ["Steam Deck review steam deck review", [3]],
                          ["review steam deck review", []],
                          ["Steam Deck review from a PC gamer", [0, 1]]])
def test_full(elasticsearch_fixture, keywords, expected_matches):
    es_fixture = elasticsearch_fixture
    es_fixture.analyze(keywords)
    results = es_fixture.search(keywords)
    matching_docs = set([int(hit["_id"]) for hit in results["hits"]["hits"]])
    assert matching_docs == set(expected_matches)
