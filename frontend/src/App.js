import { useState, useEffect, useRef } from "react";
import { fetchGet, fetchPost } from "./utils/APIUtils";
import ArticleList1 from "./components/ArticleList1";
import ArticleList2 from "./components/ArticleList2";
import FilterForm from "./components/FilterForm";
import { Routes, Route } from "react-router-dom";
import { useSessionManager } from "./utils/Auth";
import Main from "./components/Main";
import Container from "@mui/material/Container";

function App() {
  const [articleList, setArticleList] = useState([]);
  const [startDate, setStartDate] = useState('2023-11-01')
  const [endDate, setEndDate] = useState('2023-11-30')

  const sessionManager = {}
  // const sessionManager = useSessionManager();
  

  const applyFilter = async (startDate, endDate, poi, doi) => {
    console.log("applyFilter:", startDate, endDate)
    setArticleList([])
    const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}&poi=${poi}&doi=${doi}`)
    setArticleList(res.articles)

  }

  useEffect(() => {
      const getArticles = async () => {
          const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}`)
          setArticleList(res.articles)
      }

      getArticles()

  }, [])


  return (
    <Container>
      <h1 style={{ textAlign: 'center' }}>Knowledge Horizon</h1>
      <FilterForm applyFilter={applyFilter}/>
      <div style={{ textAlign: 'center', fontSize: 10 }}>Results: {articleList.length}</div>
      <Routes>
        <Route path="/" element={<ArticleList1 articleList={articleList} />} />
        <Route path="/1" element={<ArticleList1 articleList={articleList} />} />
        <Route path="/2" element={<ArticleList2 articleList={articleList} />} />
      </Routes>
    </Container>
  );
}
export default App;
