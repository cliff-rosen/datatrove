
import React from 'react';
import { Form, DatePicker, Button, Radio } from 'antd';
import moment from 'moment';

const { RangePicker } = DatePicker;

export default function ({ applyFilter }) {
    const [form] = Form.useForm();
    const dateFormat = 'YYYY/MM/DD';
    const defaultStartDate = moment('2023/11/01', dateFormat)
    const defaultEndDate = moment('2023/11/30', dateFormat)

    const formContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    };

    const onFinish = (values) => {
        console.log('Received values from form: ', values);
        const range = values.dates
        const startDate = range[0].format("YYYY-MM-DD");
        const endDate = range[1].format("YYYY-MM-DD");
        applyFilter(startDate, endDate, values.poi, values.doi);

    };

    return (
        <div style={formContainerStyle}>
            <Form form={form} 

                onFinish={onFinish} layout="inline">
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
                    <RangePicker />
                </Form.Item>
                <Form.Item
                    name="poi"
                    label="PoI"
                >   
                    <Radio.Group defaultValue='any'>
                        <Radio.Button value="any">any</Radio.Button>
                        <Radio.Button value="yes">yes</Radio.Button>
                        <Radio.Button value="no">no</Radio.Button>
                    </Radio.Group>
                </Form.Item>
                <Form.Item
                    name="doi"
                    label="DoI"
                >
                    <Radio.Group defaultValue='any'>
                        <Radio.Button value="any">any</Radio.Button>
                        <Radio.Button value="yes">yes</Radio.Button>
                        <Radio.Button value="no">no</Radio.Button>
                    </Radio.Group>
                </Form.Item>
                <Form.Item>
                    <Button htmlType="submit">
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

