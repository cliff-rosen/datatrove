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
  const sessionManager = {}
  // const sessionManager = useSessionManager();
  

  const applyFilter = async (startDate, endDate) => {
    console.log("applyFilter:", startDate, endDate)
    setArticleList([])
    const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}`)
    setArticleList(res.articles)

  }

  useEffect(() => {
      const getArticles = async () => {
          const startDate = '2024-01-01'
          const endDate = '2024-01-02'
          const res = await fetchGet(`search?startDate=${startDate}&endDate=${endDate}`)
          setArticleList(res.articles)
      }

      getArticles()

  }, [])


  return (
    <Container>
      <h1 style={{ textAlign: 'center' }}>Knowledge Horizon</h1>
      <FilterForm applyFilter={applyFilter}/>
      <Routes>
        <Route path="/" element={<ArticleList1 articleList={articleList} />} />
        <Route path="/1" element={<ArticleList1 articleList={articleList} />} />
        <Route path="/2" element={<ArticleList2 articleList={articleList} />} />
      </Routes>
    </Container>
  );
}
export default App;
