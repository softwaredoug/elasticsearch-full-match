## Elasticsearch full match

Strategies to match the phrase in a field, fully. As in :

Query: "Steam Deck Reviews"
Document1: "steam deck review"  ✅ - matches!
Document2: "steam deck review for PC gamers"  ❌ - not a match!
Document3: "Bob's steam deck review"  ❌ - not a match!

This is NOT `match_phrase` which would match these in each document.
