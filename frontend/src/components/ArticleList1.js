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

        <div>
            {articleList.map(article => (
                <Card
                    key={article.pmid}
                    title={
                        <span style={{
                            fontSize: '12px',
                            fontWeight: 'bold',
                            color: '#fff', // white text color
                            backgroundColor: '#aaa', // darker background
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
                    {article.doi === 'yes' && <Tag color="green">DoI</Tag>}
                    {article.poi === 'yes' && <Tag color="blue">PoI</Tag>}
                    <p><strong>Score:</strong> {article.score}</p>
                    <p>
                        {article.doi_list && <span><strong>DoIs:</strong> {article.doi_list}</span>}{article.doi_list && article.poi_list && <span> | </span>}
                        {article.poi_list && <span><strong>PoIs:</strong> {article.poi_list} </span>}
                    </p>
                    <p><strong>Study Outcome:</strong> {article.study_outcome} | <strong>Study Type:</strong> {article.study_type} | <strong>Systematic:</strong> {article.is_systematic}</p>
                    <p><strong>PMID:</strong> {article.pmid}</p>
                    <p><strong>Authors:</strong> {article.authors}</p>
                    <p><strong>Journal:</strong> {article.journal}</p>
                    <p><strong>Year:</strong> {article.year} | <strong>Volume:</strong> {article.volume} | <strong>Issue:</strong> {article.issue} | <strong>Pages:</strong> {article.pages}</p>
                    <p><strong>Summary:</strong> {article.summary}</p>
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