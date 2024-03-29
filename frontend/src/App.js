import { Routes, Route } from "react-router-dom";
import { useSessionManager } from "./utils/Auth";
import Nav from "./components/Nav";
import Newsletter from "./components/Newsletter";
import Workbench from "./components/Workbench";
import ArticleList1 from "./components/ArticleList1";
import FilterForm from "./components/FilterForm";
import { Layout, Divider } from 'antd';
import './App.css';

const { Header, Footer, Sider, Content } = Layout;

const layoutStyle = {
  maxWidth: '1200px',
  margin: '0 auto',
  padding: '0px',
  backgroundColor: '#fff',
}

const contentStyle = {
  padding: '0 48px',
  backgroundColor: '#fff',
};

function App() {

  const sessionManager = {}
  // const sessionManager = useSessionManager();

  return (
    <Layout style={layoutStyle}>
      <Nav />
      <Content style={contentStyle} >
        <Divider />
        <Routes>
          <Route path="/" element={<Newsletter />} />
          <Route path="/newsletter" element={<Newsletter />} />
          <Route path="/workbench" element={<Workbench />} />
        </Routes>
      </Content>
    </Layout>
  );
}
export default App;
