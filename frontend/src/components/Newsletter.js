import React from 'react';
import { useState, useEffect, useRef } from "react";
import ArticleList1 from './ArticleList1';
import { fetchGet, fetchPost } from "../utils/APIUtils";
import { Select, Divider } from 'antd';

const { Option } = Select;

export default function () {

    const startDate = '2023-11-06'
    const endDate = "2023-11-12"

    const [articleList, setArticleList] = useState([]);
    const [articleCount, setArticleCount] = useState('*')

    const applyFilter = async (startDate, endDate, poi, doi, minScore, maxScore) => {
        console.log("applyFilter:", startDate, endDate)
        setArticleCount('*')
        setArticleList([])
        const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}&poi=${poi}&doi=${doi}&minScore=${minScore}&maxScore=${maxScore}`)
        setArticleList(res.articles)
        setArticleCount(res.count)
    }

    const handleChange = (value) => {
        console.log(`selected ${value}`);
    }

    useEffect(() => {
        const getArticles = async () => {
            const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}&minScore=0&maxScore=10`)
            setArticleList(res.articles)
            setArticleCount(res.count)
        }
        getArticles()
    }, [])

    return (
        <div>
            <h2 style={{ textAlign: 'center' }}>Knowledge Horizon Newsletter for week of <Select defaultValue="11/06/23" style={{ width: 120 }} onChange={handleChange}>
                <Option value="a">11/6/23</Option>
                <Option value="b">11/13/23</Option>
                <Option value="c">11/20/23</Option>
            </Select></h2>
            <br />
            <div>
                <b>OVERVIEW</b><br />
                <br />
                The Knowledge Horizon Newsletter for the week of November 6-12, 2023, presents a comprehensive overview of recent advancements and findings predominantly focused on cardiovascular health, specifically exploring novel treatments and interventions for conditions like hypertrophic cardiomyopathy, pulmonary hypertension, cardiac amyloidosis, and heart failure. Several studies investigate the efficacy and safety of new drugs and therapeutic strategies, including the use of biomarkers and genetic variants in treatment personalization. Additionally, the issue includes research on metabolic interventions in coronary surgeries and the effects of specific compounds on renal and cardiac function. The diverse range of topics and the depth of the research highlight the newsletter's commitment to providing detailed insights into cutting-edge medical science, with a particular emphasis on cardiology and related therapeutic areas.
                <br /><br />
            </div>
            <div>
                <b>ANALYTICAL SPOTLIGHT</b><br />
                <p>
                    This week’s spotlight focuses on studies that promote an understanding of safety issues related to metabolic pathways of interest (PoI) to Palatin (i.e. natriuretic and melanocortin.) Safety reporting for the PoI’s in these publications can be summarized as follows:
                </p>
                <p>
                    <u>Melanocortin</u>
                    <br /><br />
                    30 articles out of 250 articles this week covered trials related to the melanocortin pathway, but only 1 related to safety. The study found that the melanocortin receptor pan-agonist PL9643 did not demonstrate significant treatment difference versus placebo for the primary endpoints in the overall intent-to-treat population. However, in patients with moderate or severe dry eye disease, PL9643 showed improvement in several sign endpoints and symptoms compared to placebo. There were no drug-related adverse events or discontinuations, suggesting that PL9643 is safe for use in the treatment of dry eye disease.
                </p>
                <p>
                    <u>Natriuretic</u>
                    <br /><br />
                    26 out of 250 articles this week covered trials related to the natriuretic pathway, with 7 of them related to safety. The following key takeaways were noted from those 7 studies:
                    <br /><br />
                    1.Diuretic and Natriuretic effects: The article on Boldine indicates its potential as a diuretic and natriuretic agent, which could be of considerable interest in the treatment of conditions that require the removal of excess fluid from the body, such as hypertension and congestive heart failure. The observed Ca2+-sparing effect also suggests a protective role against certain kidney stones (antiurolithiasis activity).
                    <br /><br />
                    2. Treatment strategies for acute conditions: The study on post-infarction ventricular septal rupture (VSR) highlights the importance of intervention strategy (medical, transcatheter intervention, and surgical repair) in survival outcomes. It also outlines several risk factors such as age, previous infarction, and renal function that could guide therapeutic decisions.
                    <br /><br />
                    3. Protective effects against chronic conditions: The study on alpha-lipoic acid (α-LA) demonstrates a protective role against chronic alcohol consumption-induced cardiac damage, potentially through the PINK/Parkin pathway associated with mitophagy
                </p>
            </div>
            <Divider />
            <b>ARTICLE LIST</b><br />
            <br />
            <div style={{ textAlign: 'center', fontSize: 10, margin: 10 }}>- results: {articleCount} -</div>
            <ArticleList1 articleList={articleList} />
        </div>
    )
}