def analysis():
    configured_analyzers = ["first_upper", "last_term"]

    analysis_settings = {
        "analyzer": {
            "first_upper": {
                "tokenizer": "keyword",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_keywords",
                    "english_stemmer",
                    "upper_begin",
                ]
            },
            # Get the last term
            "last_term": {
                "tokenizer": "keyword",
                "filter": [
                    "lowercase",
                    "reverse",
                    "word_delimiter",
                    "keep_first",
                    "reverse",
                    # Normal filters
                    "english_stop",
                    "english_keywords",
                    "english_stemmer",
                ]
            }
        },
        "filter": {
            "upper_begin": {
                "type": "condition",
                "filter": "uppercase",
                "script": {
                    "source": "token.position == 0"
                }
            },
            "keep_first": {
                "type": "predicate_token_filter",
                "filter": "uppercase",
                "script": {
                    "source": "token.position == 0"
                }
            },
            "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
            },
            "english_keywords": {
                "type": "keyword_marker",
                "keywords": []
            },
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english"
            },
            "english_stemmer": {
                "type": "stemmer",
                "name": "english"
            }
        }
    }
    return analysis_settings, configured_analyzer


def query(fields, keywords):
    return {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            fields[0]: keywords
                        }
                    },
                    {
                        "match": {
                            fields[1]: keywords
                        }
                    }
                ]
            }
        }
    }
