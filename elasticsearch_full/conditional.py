def analysis():
    configured_analyzer = "first_last_upper"
    analysis_settings = {
        "analyzer": {
            configured_analyzer: {
                "tokenizer": "standard",
                "char_filter": ["append_end_of_data"],
                "filter": [
                    "split_on_case_change",
                    "lowercase",
                    "upper_posn_zero",
                ]
            }
        },
        "char_filter": {
            "append_end_of_data": {
                "type": "pattern_replace",
                "pattern": "(.*)$",
                "replacement": "$1ELMO"
            }
        },
        "filter": {
            "upper_posn_zero": {
                "type": "condition",
                "filter": "upper",
                "script": {
                    "source": """
                        ((token.position == 0) ||
                         (token.term.length() > 4 && token.term.subSequence(token.term.length() - 4, token.term.length()).equals('elmo')))
                    """
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
            "upper": {
                "type": "uppercase"
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
