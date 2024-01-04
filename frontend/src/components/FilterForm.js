
import React from 'react';
import { Form, DatePicker, Button, Radio, Slider } from 'antd';
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
        const scores = values.scoreRange
        let minScore = 0
        let maxScore = 10
        if (scores) {
            console.log("scores found", scores)
            minScore = scores[0]
            maxScore = scores[1]
        }
        applyFilter(startDate, endDate, values.poi, values.doi, minScore, maxScore);

    };

    return (
        <div style={{ margin: 'auto' }}>

            <Form form={form}
                onFinish={onFinish} layout="inline"
            >
                <div>
                    <div style={formContainerStyle}>
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
                    </div>
                    <div style={{ display: 'flex' }}>
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
                    </div>
                </div>
            </Form>
        </div>
    );
};

