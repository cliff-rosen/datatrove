
import React from 'react';
import { Form, DatePicker, Button } from 'antd';
import moment from 'moment';


const { RangePicker } = DatePicker;

export default function ({applyFilter}) {
    const [form] = Form.useForm();

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
        applyFilter(startDate, endDate)
    };

    return (
        <div style={formContainerStyle}>
            <Form form={form} onFinish={onFinish} layout="inline">
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
                    <RangePicker
                        format="YYYY-MM-DD"
                        ranges={{
                            'Today': [moment(), moment()],
                            'This Month': [moment().startOf('month'), moment().endOf('month')],
                        }}
                    />
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

