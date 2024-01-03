import React from 'react';
import { useState, useEffect, useRef } from "react";
import ArticleList1 from './ArticleList1';
import FilterForm from "./FilterForm";
import { fetchGet, fetchPost } from "../utils/APIUtils";
import { Select, Divider } from 'antd';
const { Option } = Select;

export default function () {

    const startDate = '2023-11-06'
    const endDate = "2023-11-12"

    const [articleList, setArticleList] = useState([]);

    const applyFilter = async (startDate, endDate, poi, doi) => {
        console.log("applyFilter:", startDate, endDate)
        setArticleList([])
        const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}&poi=${poi}&doi=${doi}`)
        setArticleList(res.articles)

    }

    const handleChange = (value) => {
        console.log(`selected ${value}`);
    }

    useEffect(() => {
        const getArticles = async () => {
            const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}`)
            setArticleList(res.articles)
        }
        getArticles()
    }, [])

    return (
        <div style={{ maxWidth: '1000px', margin: 'auto' }}>
            <h2 style={{ textAlign: 'center' }}>Knowledge Horizon Newsletter for week of <Select defaultValue="11/06/23" style={{ width: 120 }} onChange={handleChange}>
                <Option value="a">11/6/23</Option>
                <Option value="b">11/13/23</Option>
                <Option value="c">11/20/23</Option>
            </Select></h2>
            <br />
            <div style={{ maxWidth: '1200px', margin: 'auto' }}>
                <b>OVERVIEW</b><br />
                <br />
                The Knowledge Horizon Newsletter for the week of November 6-12, 2023, presents a comprehensive overview of recent advancements and findings predominantly focused on cardiovascular health, specifically exploring novel treatments and interventions for conditions like hypertrophic cardiomyopathy, pulmonary hypertension, cardiac amyloidosis, and heart failure. Several studies investigate the efficacy and safety of new drugs and therapeutic strategies, including the use of biomarkers and genetic variants in treatment personalization. Additionally, the issue includes research on metabolic interventions in coronary surgeries and the effects of specific compounds on renal and cardiac function. The diverse range of topics and the depth of the research highlight the newsletter's commitment to providing detailed insights into cutting-edge medical science, with a particular emphasis on cardiology and related therapeutic areas.
                <br />
            </div>
            <Divider />
            <b>ARTICLE LIST</b><br />
            <FilterForm applyFilter={applyFilter} />
            <br />
            <ArticleList1 articleList={articleList} />
        </div>
    )
}