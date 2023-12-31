import { useState, useEffect, useRef } from "react";
import { fetchGet, fetchPost } from "../utils/APIUtils";
import ArticleList from "./ArticleList";

export default function Main({ sessionManager }) {

    const [articleList, setArticleList] = useState([]);

    useEffect(() => {
        const getArticles = async () => {
            const res = await fetchGet("search")
            setArticleList(res.articles)
        }

        getArticles()

    }, [])

    if (articleList.length == 0) return <div>*</div>

    return (
              <ArticleList
                articleList={articleList}
              />
    )};
    

