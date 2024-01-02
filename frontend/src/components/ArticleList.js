import React from 'react';
import { Card, Tag, Button, Row, Col, Collapse } from 'antd';


export default function ({ articleList }) {
    console.log(articleList)
    const { Panel } = Collapse;

    const copyToClipboard = (title, abstract) => {
        const textToCopy = `Title: ${title}\nAbstract: ${abstract}`;
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert('Copied to clipboard!'); // You can replace this with a more subtle notification
        }, (err) => {
            console.error('Error copying text: ', err);
        });
    };

    return (

        <div style={{ maxWidth: '800px', margin: 'auto' }}>
            <h1 style={{ textAlign: 'center' }}>PubMed Search Results</h1>
                {articleList.map(article => (
                <Card
                    key={article.PMID}
                    title={
                        <span style={{ 
                            fontSize: '14px', 
                            fontWeight: 'bold', 
                            color: '#fff', // white text color
                            backgroundColor: '#888', // darker background
                            display: 'block',
                            padding: '2px 2px' // optional padding
                        }}>
                            {article.title}
                        </span>
                    }                    
                    style={{ marginBottom: '10px' }}
                    type="inner"
                    extra={<Button onClick={() => copyToClipboard(article.title, article.abstract)}>Copy</Button>} // Add Copy button here

                >
                    <Tag color="green">DoI</Tag><Tag color="blue">PoI</Tag>
                    <p><strong>Authors:</strong> {article.authors}</p>
                    <p><strong>Journal:</strong> {article.journal} | <strong>Year:</strong> {article.year}</p>
                    <p><strong>Volume:</strong> {article.volume} | <strong>Issue:</strong> {article.issue} | <strong>Pages:</strong> {article.pages}</p>
                    <Collapse bordered={false} ghost>
                        <Panel header="Abstract" key="1">
                            <p>{article.abstract}</p>
                        </Panel>
                    </Collapse>
                </Card>
            ))}
        </div>

    )

}