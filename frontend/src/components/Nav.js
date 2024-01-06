import React, {useState} from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { Layout, Space, Typography, Menu, MenuProps } from 'antd';
//import 'antd/dist/antd.css'; // Import Ant Design CSS

const { Header } = Layout;
const items = [
    {
      label: 'Newsletter',
      key: 'newsletter',
    },
    {
      label: 'Workbench',
      key: 'workbench',
    }]

const Nav = () => {
    console.log("Nav render");
    const navigate = useNavigate();
    const location = useLocation();
    const [current, setCurrent] = useState('mail');

    const onClick = (e) => {
        console.log('click ', e);
        setCurrent(e.key);
        navigate(`/${e.key}`)
      };

    return (
        <Header
            style={{
                display: "flex",
                alignItems: "center",
                paddingTop: 10,
                paddingBottom: 10,
                border: "none",
                background: "white"
            }}
        >
            <Typography.Title level={4} style={{ margin: 0 }}>
                <Link to="/" style={{ textDecoration: "none" }}>
                    <img src="logo1.png" alt="Knowledge Horizon" style={{ width: 250, height: 50, marginRight: 10 }} />
                </Link>
            </Typography.Title>

            <div style={{ minWidth: 20 }}></div>

            <div
                style={{
                    flexGrow: 1,
                    color: "red",
                    border: "none",
                }}
            >
            </div>

            <div style={{ flexGrow: 0, fontSize: "1em" }}>
            <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
            </div>
        </Header>
    );
};

export default Nav;
