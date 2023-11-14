
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

