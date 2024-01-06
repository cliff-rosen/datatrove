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

            <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
    );
};

export default Nav;
