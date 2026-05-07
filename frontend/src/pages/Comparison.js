import React, { useState } from 'react';
import { Card, Row, Col, Select, Button, Table, Tag, Statistic } from 'antd';
import { SwapOutlined, DownloadOutlined } from '@ant-design/icons';
import ReactEcharts from 'echarts-for-react';

const { Option } = Select;

const Comparison = () => {
  const [products, setProducts] = useState(['本产品', '竞品A', '竞品B']);

  const radarOption = {
    title: { text: '多维度对比雷达图', left: 'center' },
    tooltip: {},
    legend: { bottom: 0 },
    radar: {
      indicator: [
        { name: '性价比', max: 100 },
        { name: '质量', max: 100 },
        { name: '外观', max: 100 },
        { name: '服务', max: 100 },
        { name: '物流', max: 100 },
        { name: '功能', max: 100 }
      ]
    },
    series: [{
      type: 'radar',
      data: [
        { value: [85, 88, 90, 75, 70, 82], name: '本产品', areaStyle: { opacity: 0.3 } },
        { value: [78, 85, 80, 82, 75, 80], name: '竞品A', areaStyle: { opacity: 0.3 } },
        { value: [82, 80, 85, 78, 72, 75], name: '竞品B', areaStyle: { opacity: 0.3 } }
      ]
    }]
  };

  const barOption = {
    title: { text: '各维度得分对比', left: 'center' },
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0 },
    xAxis: { type: 'category', data: ['性价比', '质量', '外观', '服务', '物流', '功能'] },
    yAxis: { type: 'value', max: 100 },
    series: [
      { name: '本产品', type: 'bar', data: [85, 88, 90, 75, 70, 82], itemStyle: { color: '#1890ff' } },
      { name: '竞品A', type: 'bar', data: [78, 85, 80, 82, 75, 80], itemStyle: { color: '#52c41a' } },
      { name: '竞品B', type: 'bar', data: [82, 80, 85, 78, 72, 75], itemStyle: { color: '#faad14' } }
    ]
  };

  const heatmapOption = {
    title: { text: '槽点重叠度热力图', left: 'center' },
    tooltip: { position: 'top' },
    grid: { height: '50%', top: '10%' },
    xAxis: { type: 'category', data: ['本产品', '竞品A', '竞品B'] },
    yAxis: { type: 'category', data: ['物流', '售后', '价格', '质量', '包装'] },
    visualMap: { min: 0, max: 100, calculable: true, orient: 'horizontal', left: 'center', bottom: '15%' },
    series: [{
      type: 'heatmap',
      data: [
        [0, 0, 85], [0, 1, 75], [0, 2, 60], [0, 3, 40], [0, 4, 30],
        [1, 0, 70], [1, 1, 80], [1, 2, 55], [1, 3, 45], [1, 4, 35],
        [2, 0, 75], [2, 1, 78], [2, 2, 50], [2, 3, 42], [2, 4, 25]
      ],
      label: { show: true }
    }]
  };

  const comparisonData = [
    { key: '1', dimension: '性价比', ourProduct: 85, competitorA: 78, competitorB: 82, winner: 'our' },
    { key: '2', dimension: '质量', ourProduct: 88, competitorA: 85, competitorB: 80, winner: 'our' },
    { key: '3', dimension: '外观', ourProduct: 90, competitorA: 80, competitorB: 85, winner: 'our' },
    { key: '4', dimension: '服务', ourProduct: 75, competitorA: 82, competitorB: 78, winner: 'competitorA' },
    { key: '5', dimension: '物流', ourProduct: 70, competitorA: 75, competitorB: 72, winner: 'competitorA' },
    { key: '6', dimension: '功能', ourProduct: 82, competitorA: 80, competitorB: 75, winner: 'our' }
  ];

  const columns = [
    { title: '维度', dataIndex: 'dimension', key: 'dimension', width: 100 },
    { 
      title: '本产品', 
      dataIndex: 'ourProduct', 
      key: 'ourProduct', 
      width: 100,
      sorter: (a, b) => a.ourProduct - b.ourProduct,
      render: (val) => <span style={{ color: '#1890ff', fontWeight: 'bold' }}>{val}</span>
    },
    { 
      title: '竞品A', 
      dataIndex: 'competitorA', 
      key: 'competitorA', 
      width: 100,
      sorter: (a, b) => a.competitorA - b.competitorA,
      render: (val) => <span style={{ color: '#52c41a' }}>{val}</span>
    },
    { 
      title: '竞品B', 
      dataIndex: 'competitorB', 
      key: 'competitorB', 
      width: 100,
      sorter: (a, b) => a.competitorB - b.competitorB,
      render: (val) => <span style={{ color: '#faad14' }}>{val}</span>
    },
    { 
      title: '领先产品', 
      key: 'winner', 
      width: 100,
      render: (_, record) => {
        const config = {
          our: { color: 'blue', text: '本产品' },
          competitorA: { color: 'green', text: '竞品A' },
          competitorB: { color: 'orange', text: '竞品B' }
        };
        const { color, text } = config[record.winner];
        return <Tag color={color}>{text}</Tag>;
      }
    }
  ];

  return (
    <div>
      <Card style={{ marginBottom: 24 }}>
        <Row justify="space-between" align="middle">
          <Col>
            <h3 style={{ margin: 0 }}>竞品对比分析</h3>
          </Col>
          <Col>
            <Button type="primary" icon={<DownloadOutlined />}>
              导出对比报告
            </Button>
          </Col>
        </Row>
      </Card>

      <Row gutter={[24, 24]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={12}>
          <Card title="雷达图对比">
            <ReactEcharts option={radarOption} style={{ height: 400 }} />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="柱状图对比">
            <ReactEcharts option={barOption} style={{ height: 400 }} />
          </Card>
        </Col>
      </Row>

      <Card title="详细数据对比" style={{ marginBottom: 24 }}>
        <Table 
          columns={columns} 
          dataSource={comparisonData} 
          pagination={false}
          size="middle"
        />
      </Card>

      <Card title="槽点重叠度热力图">
        <ReactEcharts option={heatmapOption} style={{ height: 400 }} />
      </Card>
    </div>
  );
};

export default Comparison;
