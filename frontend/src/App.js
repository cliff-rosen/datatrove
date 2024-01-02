import { useState, useEffect, useRef } from "react";
import { fetchGet, fetchPost } from "./utils/APIUtils";
import ArticleList1 from "./components/ArticleList1";
import ArticleList2 from "./components/ArticleList2";
import { Routes, Route } from "react-router-dom";
import { useSessionManager } from "./utils/Auth";
import Main from "./components/Main";
import Container from "@mui/material/Container";

function App() {
  const [articleList, setArticleList] = useState([]);
  const sessionManager = {}
  // const sessionManager = useSessionManager();
  
  useEffect(() => {
      const getArticles = async () => {
          const res = await fetchGet("search")
          setArticleList(res.articles)
      }

      getArticles()

  }, [])


  return (
    <Container>
      <Routes>
        <Route path="/1" element={<ArticleList1 articleList={articleList} />} />
        <Route path="/2" element={<ArticleList2 articleList={articleList} />} />
      </Routes>
    </Container>
  );
}
export default App;
