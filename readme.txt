
TO DO:

implement basic workflow in google sheet
    articles = getArticles()
    (scoring_prompt, score_prompt_improvement_prompt) = getPrompts()

    for article_id in len(articles)

        score = getScore(article_id, scoring_prompt)
        writeScore(article_id, score)

        scoring_prompt = updatePrompt(article_id, scoring_prompt, score_prompt_improvement_prompt, score)

        scores = getScores(article_id, scoring_prompt)
        writeScores(article_id)

possibly try having a "rules" section of scoring prompt that gets updated instead of updating entire prompt


get samples
get prompts
model score first article
record score
update prompt
model score first article
record score
record prompt


------------------------------------------

- implement 'enhance prompt'; store prior prompts to browse or revert
- feature to rescore all and report on loss
- where to store and when to update prompts
- UI disables when waiting for llm
- store user edited human scores

Article (records[index])
- PMID
- Title
- Abstract
Human Score
- Score
- Explanation
Machine Score
- Score
- Explanation
Prompts
- Current
- Updated


Inputs:
- human provided mandate
- N number of examples with human scoring
- create initial prompt prompt

Retrieve 3 prompts:
- create initial scoring prompt
- scoring prompt
- scoring prompt training prompt

1. Init
Retrieve all abstracts from target sheet
Retrieve all prompts

2. Generate initial scoring prompt

3. Loop through abstracts
next_abstract = get_next()
while next_abstract:
    p_score = get_score(abstract)
    display abstract:
        title, abstract, h_score, p_score
    new_draft = update_draft(cur_draft, title, abstract, h_score, p_score)
    display new_draft
    user revises/accepts/test new draft
    next_abstract = get_next()

User should be able to walk through all abstracts and see:
- title, abstract, human score
- scoring_prompt_init, p_score
- scoring_prompt_adj, p_score_adj

User can compare:
- human mandate
- scoring_prompt_t
- abstract, h_score, p_score_t

