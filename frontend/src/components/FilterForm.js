import React, { useState } from 'react';
import { Form, Space, DatePicker, Button, Radio, Slider } from 'antd';
import moment from 'moment';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';

dayjs.extend(customParseFormat);

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
const defaultStartDate = '2023/11/01'
const defaultEndDate = '2023/11/30'


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
            layout='vertical'
            initialValues={{
                dates: [dayjs(defaultStartDate, dateFormat), dayjs(defaultEndDate, dateFormat)]
            }}
        >

            <Form.Item
                name="dates"
                label="Start and End Date"
                rules={[
                    {
                        type: 'array',
                        required: true,
                        message: 'Please select start and end date!'
                    }
                ]}
            >
                <RangePicker/>
            </Form.Item>

            <Form.Item
                name="poi"
                label="PoI"
            >
                <Radio.Group defaultValue='any'>
                    <Space direction='vertical'>
                        <Radio value="any">any</Radio>
                        <Radio value="yes">yes</Radio>
                        <Radio value="no">no</Radio>
                    </Space>
                </Radio.Group>
            </Form.Item>

            <Form.Item
                name="doi"
                label="DoI"
            >
                <Radio.Group defaultValue='any'>
                    <Space direction='vertical'>
                        <Radio value="any">any</Radio>
                        <Radio value="yes">yes</Radio>
                        <Radio value="no">no</Radio>
                    </Space>
                </Radio.Group>
            </Form.Item>
            <Form.Item
                name="scoreRange"
                label="Score Range"
                style={{ flex: 5, marginRight: 50 }}
            >
                <Slider range min={0} max={10} defaultValue={[0, 10]} />
            </Form.Item>

            <Form.Item>
                <Button htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

