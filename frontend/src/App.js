import { Routes, Route } from "react-router-dom";
import { useSessionManager } from "./utils/Auth";
import Nav from "./components/Nav";
import Newsletter from "./components/Newsletter";
import Workbench from "./components/Workbench";
import ArticleList1 from "./components/ArticleList1";
import FilterForm from "./components/FilterForm";
import { Divider } from 'antd';
import Container from "@mui/material/Container";


function App() {

  const sessionManager = {}
  // const sessionManager = useSessionManager();
  
  return (
    <Container>
      <Nav/>
      <Routes>
        <Route path="/" element={<Newsletter />} />
        <Route path="/newsletter" element={<Newsletter />} />
        <Route path="/workbench" element={<Workbench/>} />
      </Routes>
    </Container>
  );
}
export default App;
