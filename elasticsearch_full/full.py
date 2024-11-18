def analysis_settings():
    return {
            "analyzer": {
                "case_split_english": {
                    "tokenizer": "standard",
                    "filter": [
                        "split_on_case_change",
                        "lowercase",
                        "stop",
                        "english_stemmer"
                    ]
                }
            },
            "filter": {
                "split_on_case_change": {
                    "type": "word_delimiter_graph",
                    "split_on_case_change": True
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "name": "english"
                }
            }
        },


def query(field, keywords):
    return {
        "query": {
            "match_phrase": {
                "field": {
                    "query": keywords
                }
            }
        }
    }
