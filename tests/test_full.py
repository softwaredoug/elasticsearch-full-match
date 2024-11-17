"""Tests a full field match - defined by every query token matching every position and nothing else."""
import pytest
from elasticsearch_full.shingles import analysis, query
from elasticsearch import Elasticsearch


def _analyze(es, text, analyzer):
    response = es.indices.analyze(
        index="test-index",
        body={
            "analyzer": analyzer,
            "text": text
        }
    )
    return "__".join([token["token"] for token in response["tokens"]])


def create_index(index):
    es = Elasticsearch("http://localhost:9200")
    es.indices.delete(index=index, ignore=[400, 404])
    analysis_settings, configured_analyzer = analysis()
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
                    "analyzer": configured_analyzer
                }
            }
        }
    }
    es.indices.create(index=index, body=settings)
    print("Analyzed with:", configured_analyzer)
    print(_analyze(es,
                   "SteamDeck review from a PC gamer",
                   configured_analyzer))
    return es


def index_docs(es, docs):
    for id, doc in enumerate(docs):
        es.index(index="test-index",
                 id=id,
                 body={"title": doc})
    es.indices.refresh(index="test-index")


@pytest.fixture(scope="module")
def setup_es():
    es = create_index("test-index")
    docs = [
        "SteamDeck review from a PC gamer",
        "steam deck review from a PC gamer",
        "Steam Deck review",
        "Steam Deck",
        "Steam",
    ]
    index_docs(es, docs)
    return es


@pytest.mark.parametrize("keywords, expected_matches",
                         [["Steam", [4]],
                          ["Steam Deck", [3]],
                          ["Steam Deck review", [2]],
                          ["Steam Deck review from a PC gamer", [0, 1]]])
def test_full(setup_es, keywords, expected_matches):
    results = setup_es.search(index="test-index", body=query("title", keywords))
    matching_docs = set([int(hit["_id"]) for hit in results["hits"]["hits"]])
    assert matching_docs == set(expected_matches)
