def analysis():
    """Configure as keyword field."""
    configured_analyzer = "sentinel_tokens"
    analysis_settings = {
        "char_filter": {
            "sentinel_tokens": {
                "type": "pattern_replace",
                "pattern": "^(.*)$",
                "replacement": "__SENTINEL_BEGIN__ $1 __SENTINEL_END__"
            }
        },
        "filter": {
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
        },
        "analyzer": {
            configured_analyzer: {
                "char_filter": ["sentinel_tokens"],
                "tokenizer": "standard",
                "filter": [
                    "english_possessive_stemmer",
                    "lowercase",
                    "english_stop",
                    "english_keywords",
                    "english_stemmer"
                ]
            }
        }
    }
    return analysis_settings, configured_analyzer


def query(field, keywords):
    """Query for keyword field."""
    return {
        "query": {
            "match_phrase": {
                field: keywords
            }
        }
    }
