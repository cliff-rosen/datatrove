import React from 'react';
import { useState, useEffect, useRef } from "react";
import FilterForm from "./FilterForm";
import { fetchGet, fetchPost } from "../utils/APIUtils";
import { Divider } from 'antd';
import { Card, Tag, Button, Row, Col, Collapse } from 'antd';
import ArticleList2 from './ArticleList2';

const filterObjDefault = {
    startDate: '2023-11-01',
    endDate: '2023-11-30',
    poi: 'any',
    doi: 'any',
    minScore: 0,
    maxScore: 0
}

export default function () {
    const [articleList, setArticleList] = useState([]);
    const [articleCount, setArticleCount] = useState('*')
    const [startDate, setStartDate] = useState('2023-11-01')
    const [endDate, setEndDate] = useState('2023-11-30')
    const { Panel } = Collapse;

    const applyFilter = async ({ startDate, endDate, poi, doi, minScore, maxScore }) => {
        console.log("applyFilter:", startDate, endDate)
        setArticleCount('***')
        setArticleList([])
        const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}&poi=${poi}&doi=${doi}&minScore=${minScore}&maxScore=${maxScore}`)
        setArticleList(res.articles)
        setArticleCount(res.count)
    }

    return (

        <div style={{ margin: 'auto', display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>

            <FilterForm applyFilter={applyFilter} />
            <Divider />
            <div style={{ textAlign: 'center', fontSize: 10, margin: 10 }}>- results: {articleCount} -</div>
            <ArticleList2 articleList={articleList} />
        </div>
    )
}