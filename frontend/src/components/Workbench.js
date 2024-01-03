import React from 'react';
import { useState, useEffect, useRef } from "react";
import FilterForm from "./FilterForm";
import { fetchGet, fetchPost } from "../utils/APIUtils";
import { Divider } from 'antd';
import { Card, Tag, Button, Row, Col, Collapse } from 'antd';
import ArticleList1 from './ArticleList1';


export default function () {
    const [articleList, setArticleList] = useState([]);
    const [startDate, setStartDate] = useState('2023-11-01')
    const [endDate, setEndDate] = useState('2023-11-30')
    const { Panel } = Collapse;
    
    const applyFilter = async (startDate, endDate, poi, doi) => {
      console.log("applyFilter:", startDate, endDate)
      setArticleList([])
      const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}&poi=${poi}&doi=${doi}`)
      setArticleList(res.articles)
  
    }
  
    const copyToClipboard = (title, abstract) => {
        const textToCopy = `Title: ${title}\nAbstract: ${abstract}`;
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert('Copied to clipboard!'); // You can replace this with a more subtle notification
        }, (err) => {
            console.error('Error copying text: ', err);
        });
    };


    useEffect(() => {
        const getArticles = async () => {
            const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}`)
            setArticleList(res.articles)
        }
  
        getArticles()
  
    }, [])
  
    return (

        <div style={{ maxWidth: '1200px', margin: 'auto' }}>
            <FilterForm applyFilter={applyFilter} />
            <Divider />
            <div style={{ textAlign: 'center', fontSize: 10, margin: 10 }}>- results: {articleList.length} -</div>
            <ArticleList1 articleList={articleList} />
        </div>
    )
}