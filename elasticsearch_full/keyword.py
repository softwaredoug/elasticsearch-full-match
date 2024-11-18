def analysis():
    """Configure as keyword field."""
    configured_analyzer = "keyword"
    analysis_settings = {
        "analyzer": {
            configured_analyzer: {
                "tokenizer": "keyword",
                "filter": ["lowercase"]
            }
        }
    }
    return analysis_settings, configured_analyzer


def query(field, keywords):
    """Query for keyword field."""
    return {
        "query": {
            "match": {
                field: keywords
            }
        }
    }
