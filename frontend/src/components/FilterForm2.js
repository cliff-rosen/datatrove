import React, { useState } from 'react';
import { Form, Space, DatePicker, Button, Radio, Slider } from 'antd';
import moment from 'moment';

const { RangePicker } = DatePicker;
const filterObjDefault = {
    startDate: '2023-11-01',
    endDate: '2023-11-30',
    poi: 'any',
    doi: 'any',
    minScore: 0,
    maxScore: 0
}
const dateFormat = 'YYYY/MM/DD';
const defaultStartDate = moment('2023/11/01', dateFormat)
const defaultEndDate = moment('2023/11/30', dateFormat)


export default function ({ applyFilter }) {
    const [filterObj, setFilterObj] = useState(filterObjDefault)
    const [form] = Form.useForm();

    const formContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column'
    };

    const onFinish = (values) => {
        console.log('Received values from form: ', values);
        const range = values.dates
        const startDate = range[0].format("YYYY-MM-DD");
        const endDate = range[1].format("YYYY-MM-DD");
        const scores = values.scoreRange
        let minScore = 0
        let maxScore = 10
        if (scores) {
            console.log("scores found", scores)
            minScore = scores[0]
            maxScore = scores[1]
        }
        applyFilter({ startDate, endDate, poi: values.poi, doi: values.doi, minScore, maxScore });

    };

    return (
        <Form form={form}
            onFinish={onFinish}
        >
            <Form.Item
                name="poi"
                label="PoI"
            >
                <Radio.Group defaultValue='any' xsize='large'>
                    <Space direction="vertical">
                        <Radio value="any">any</Radio>
                        <Radio value="yes">yes</Radio>
                        <Radio value="no">no</Radio>
                    </Space>
                </Radio.Group>
            </Form.Item>
        </Form>
    );
};

