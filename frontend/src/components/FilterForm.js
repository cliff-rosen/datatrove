import React, { useState, useRef } from 'react';
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
    maxScore: 10
}

const dateFormat = 'YYYY/MM/DD';
const defaultStartDate = '2023/11/01'
const defaultEndDate = '2023/11/30'


export default function ({ applyFilter, resetArticleList }) {
    const [filterObj, setFilterObj] = useState(filterObjDefault)
    const formRef = useRef(null); // Create a ref for the form
    const [form] = Form.useForm();

    const clearForm = () => {
        formRef.current.resetFields()
        resetArticleList()
        // formRef.current.setFieldsValue({
        //     dates: [dayjs(), dayjs()] // Sets both start and end dates to today
        // });
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
            ref={formRef}
            onFinish={onFinish}
            layout='vertical'
            initialValues={{
                dates: [dayjs(defaultStartDate, dateFormat), dayjs(defaultEndDate, dateFormat)],
                scoreRange: [0, 10]
            }}
        >

            <Form.Item
                ref={formRef} 
                name="dates"
                className="bold-label"
                label="DATES"
                rules={[
                    {
                        type: 'array',
                        required: false,
                        message: 'Please select start and end date!'
                    }
                ]}
            >
                <RangePicker/>
            </Form.Item>

            <Form.Item
                name="poi"
                className="bold-label"                
                label="POI"
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
                className="bold-label"                
                label="DOI"
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
                className="bold-label"
                label="SCORE RANGE"
                style={{ flex: 5, marginRight: 50 }}
            >
                <Slider range min={0} max={10} />
            </Form.Item>

            <Form.Item>
                <Button htmlType="submit">
                    Submit
                </Button>
                <Button
                    style={{ marginLeft: '10px' }}
                    onClick={clearForm}
                >
                    Clear
                </Button>
            </Form.Item>

        </Form>
    );
};

