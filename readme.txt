
TO DO:

add title to abstract when sending to llm
json should return pathways and diseases

for prompt:
- identify features that drive score. s = f(f1, f2, ...)
- define rules that correlate features with score
- if rules too complicated, rethink features; abstract at higher level

go through giovanni's responses and try to identify features and rules
all aspects of pathways or just some?
all aspects of diseases or just some?
treatment and diagnostics?

iterate on improvement prompt
structure prompt as:
- models role
- business details
- general scoring guidelines
- specific scoring rules (these are what get updated)
try getting better instructions so the model understands the role of the prompts, human scorer, etc.
consider getting rules updated based on groups of abstract-scoring pairs rather than one at a time

algorithm:
- prompt includes a designated rules section
- rules section is seeded by initial prompt + human mandate
- rules are updated as follows:
a. model analyzes abstract, human score, machine score and prompt and suggests update to rules. response is rules changes plus explanation
b. model analyzes prompt and suggested changes and returns updated prompt

when analyzing performance review models logic for changes and see if the rules delta is sensible given human scores. also make sure human scores are consistent so that if article x is rewarded according to a certain rule then article y should also be rewarded for that rule.

it should be the case that the human score explanation plus the delta between the human score and machine score yields a sensible rule delta. review logs to see if this is the case.

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

-------------

TABLE OF DEFINITIONS
Term: Definition
PoI: Pathway of Interest (i.e. melanocortin, natriuretic pathways)
Do: Disease of Interest (i.e. dry eye, ulcerative colitis, crohn's disease, retinopathy, retinal disease)
Human studies: randomized controlled clinical trials (RCTs), epidemiological studies, open label trials, and case reports
Non-human studies: animal studies, in vitro studies, computer modeling
RCT	randomized controlled clinical trials

FEATURE	DOMAIN OF VALUES
PoI Rel	yes, no
DoI Rel	yes, no
Is Systematic	yes, no
Study Type	animal, human RCT, human non-RCT, in vitro, other, not a study
Study Outcome	effectiveness, safety, bio marker, other

Please set feature values for the below abstract according to the following instructions. Each abstract has the following list of feature:

- pathway_rel [yes, no]: Set to yes if the abstract relates to either the melanocortin or natriuretic metabolic pathway, and otherwise set to no

- disease_rel [yes, no]: Set to yes if the abstract relates to either the melanocortin or natriuretic metabolic pathway, and otherwise set to dry eye, ulcerative colitis, crohn's disease, retinopathy or retinal disease, and otherwise set to no

- is_systematic [yes, no]: Set to yes if the abstract relates to a systematic review or a meta study and otherwise set to no

- study_type [animal, human RCT, human non-RCT, in vitro, other, not a study]: set to whichever allowed value best matches the study described in the abstract

- study_outcome [effectiveness, safety, bio marker]: return a list of any allowed value that applies to the outcomes targeted in the abstract

Return your answer in the following JSON format:

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "pathway_rel": {
      "type": "string",
      "description": "Set to 'yes' if the abstract relates to either the melanocortin or natriuretic metabolic pathway, otherwise set to 'no'.",
      "enum": ["yes", "no"]
    },
    "disease_rel": {
      "type": "string",
      "description": "Set to 'yes' if the abstract relates to dry eye, ulcerative colitis, Crohn's disease, retinopathy or retinal disease, otherwise set to 'no'.",
      "enum": ["yes", "no"]
    },
    "is_systematic": {
      "type": "string",
      "description": "Set to 'yes' if the abstract is a systematic review or a meta-study, otherwise set to 'no'.",
      "enum": ["yes", "no"]
    },
    "study_type": {
      "type": "string",
      "description": "Set to the type of study described in the abstract. Choose from 'animal', 'human RCT', 'human non-RCT', 'in vitro', 'other', or 'not a study'.",
      "enum": ["animal", "human RCT", "human non-RCT", "in vitro", "other", "not a study"]
    },
    "study_outcome": {
      "type": "array",
      "description": "List any outcomes targeted in the abstract. Allowed values are 'effectiveness', 'safety', and 'bio marker'.",
      "items": {
        "type": "string",
        "enum": ["effectiveness", "safety", "bio marker"]
      }
    }
  },
  "required": ["pathway_rel", "disease_rel", "is_systematic", "study_type", "study_outcome"]
}



PoI Rel	yes, no
DoI Rel	yes, no
Is Systematic	yes, no
Study Type	animal, human RCT, human non-RCT, in vitro, other, not a study
Study Outcome	effectiveness, safety, bio marker, other





TABLE OF SCORES
Score	Article Characeteristic
1	Article fails to address PoI OR DoI in any way
2	Article fails to address any therapeutic value of PoI AND fails to address diagnostic markers relevant to DoI AND fails to provide a systematic review or meta analysis of DoI
3	Article addresses therapeutic value of PoI in non-human studies but not in relation to DoI
4	Article addresses therapeutic value of PoI in human studies but not in relation to DoI
5	Article fails to address therapeutic value of PoI but it does provide information relevant to DoI (but NOT systematic review or meta analysis)
6	Article fails to address therapeutic value of PoI but it does provide information relevant to DoI in the form of a systematic review or meta analysis
7	Article addresses PoI AND DoI in human, animal, or in vitro studies, but NOT in the context of safety or efficacy
8	Article addresses safety of PoI in human studies or non-human studies but NOT in the context of efficacy for DoI
9	"Article addresses therapeutic value of PoI in the context of efficacy for DoI using human studies, but NOT RCTs
OR
Article addresses therapeutic value of PoI in the context of efficacy using non-human studies"
10	Article addresses therapeutic value of PoI in the context of efficacy for DoI using randomized clinical trial (RCT) methodology
	

