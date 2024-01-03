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
            {articleList.map(article => (
                <Card
                    key={article.pmid}
                    title={article.title}
                    style={{ marginBottom: '10px' }}
                    type="inner"
                    extra={<Button onClick={() => copyToClipboard(article.title, article.abstract)}>Copy</Button>} // Add Copy button here
                >
                    <strong>Score:</strong> {article.score} {article.doi === 'yes' && <Tag color="green">DoI</Tag>} {article.poi === 'yes' && <Tag color="blue">PoI</Tag>}
                    <br />
                    {article.doi_list && <span><strong>DoIs:</strong> {article.doi_list}</span>}{article.doi_list && article.poi_list && <span> | </span>}
                    {article.poi_list && <span><strong>PoIs:</strong> {article.poi_list} </span>}
                    <br />
                    <strong>Study Outcome:</strong> {article.study_outcome} | <strong>Study Type:</strong> {article.study_type} | <strong>Sys/Meta:</strong> {article.is_systematic}
                    <br /><br />
                    {article.authors} {article.title}. {article.journal}. {article.year};{article.volume}({article.issue}):{article.pages}"
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