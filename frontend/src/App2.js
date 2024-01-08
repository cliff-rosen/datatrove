import React from 'react';
import { Layout, Menu } from 'antd';

const { Header, Content, Sider } = Layout;

const App = () => (
    <Layout>
        <Header>
            <span style={{color: 'fff'}}>header</span>
        </Header>
        <Layout>
            <Sider width={200}>
                Sider
            </Sider>
            <Layout style={{ padding: '0 24px 24px' }}>
                <Content
                    style={{
                        padding: 24,
                        margin: 0,
                        minHeight: 280,
                    }}
                >
                    content
                </Content>
            </Layout>
        </Layout>
    </Layout>
);

export default App;
