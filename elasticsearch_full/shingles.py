def analysis():
    configured_analyzer = "case_split_english_concat"
    analysis_settings = {
        "analyzer": {
            configured_analyzer: {
                "tokenizer": "standard",
                "filter": [
                    "split_on_case_change",
                    "lowercase",
                    "stop",
                    "english_stemmer",
                    "big_shingles",
                    "only_position_zero",
                    "shingle_fingerprint"
                ]
            }
        },
        "filter": {
            "only_position_zero": {
                "type": "predicate_token_filter",
                "script": {
                    "source": "token.position == 0"
                },
            },
            "split_on_case_change": {
                "type": "word_delimiter_graph",
                "split_on_case_change": True
            },
            "english_stemmer": {
                "type": "stemmer",
                "name": "english"
            },
            "big_shingles": {
                "type": "shingle",
                "min_shingle_size": 2,
                "max_shingle_size": 10
            },
            "shingle_fingerprint": {
                "type": "fingerprint",
                "max_output_size": 1000,
                "separator": "+"
            }
        }
    }
    return analysis_settings, configured_analyzer


def query(field, keywords):
    return {
        "query": {
            "match_phrase": {
                field: keywords
            }
        }
    }
