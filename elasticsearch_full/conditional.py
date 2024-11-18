END_OF_DATA = "SENTINELENDOFDATA"


def analysis():
    configured_analyzer = "first_upper"
    analysis_settings = {
        "analyzer": {
            configured_analyzer: {
                "char_filter": ["append_sentinel"],
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_keywords",
                    "english_stemmer",
                    "upper_begin",
                ]
            }
        },
        # Possible way of marking last term?
        "char_filter": {
            "append_end_of_data": {
                "type": "pattern_replace",
                "pattern": "(^.*$)",
                "replacement": f"$1{END_OF_DATA}"
            },
            "append_sentinel": {
                "type": "pattern_replace",
                "pattern": "(^.*$)",
                "replacement": f"$1 {END_OF_DATA}"
            }
        },
        "filter": {
            # Could we remove this?
            "remove_end_of_data": {
                "type": "pattern_replace",
                "pattern": f"(^.*?){END_OF_DATA}$",
                "replacement": "$1"
            },
            # Then uppercase it before stemming, etc?
            # Sadly when we do this, the upper cased term is not stemmed
            "mark_begin_end": {
                "type": "condition",
                "filter": "uppercase",
                "script": {
                    "source": f"""
                        ((token.position == 0) ||
                         (token.term.length() > {len(END_OF_DATA)}
                          && token.term.subSequence(token.term.length() - {len(END_OF_DATA)}, token.term.length()).equals('{END_OF_DATA.lower()}')))
                    """
                },
            },
            "upper_begin": {
                "type": "condition",
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


def query(field, keywords):
    return {
        "query": {
            "match_phrase": {
                field: keywords
            }
        }
    }
