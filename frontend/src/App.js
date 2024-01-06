import { Routes, Route } from "react-router-dom";
import { useSessionManager } from "./utils/Auth";
import Nav from "./components/Nav";
import Newsletter from "./components/Newsletter";
import Workbench from "./components/Workbench";
import ArticleList1 from "./components/ArticleList1";
import FilterForm from "./components/FilterForm";
import { Divider } from 'antd';
import Container from "@mui/material/Container";
import './App.css';


function App() {

  const sessionManager = {}
  // const sessionManager = useSessionManager();

  return (
    <div>
      <Nav style={{ "border": 1 }} />
      <Routes>
        <Route path="/" element={<Newsletter />} />
        <Route path="/newsletter" element={<Newsletter />} />
        <Route path="/workbench" element={<Workbench />} />
      </Routes>
    </div>
  );
}
export default App;
