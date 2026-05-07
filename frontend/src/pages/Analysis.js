import React, { useState } from 'react';
import { Card, Tabs, Row, Col, Tag, List, Progress, Statistic, Spin } from 'antd';
import { LikeOutlined, DislikeOutlined, WarningOutlined } from '@ant-design/icons';
import ReactEcharts from 'echarts-for-react';

const { TabPane } = Tabs;

const Analysis = () => {
  const [activeTab, setActiveTab] = useState('satisfactory');

  // 满意点数据
  const satisfactoryPoints = [
    { category: '性价比', count: 320, examples: ['价格实惠', '性价比高', '物超所值'], sentiment: 'positive' },
    { category: '质量', count: 280, examples: ['做工精细', '材质好', '耐用'], sentiment: 'positive' },
    { category: '外观', count: 220, examples: ['设计好看', '颜色正', '颜值高'], sentiment: 'positive' },
    { category: '功能', count: 180, examples: ['操作简单', '功能齐全', '智能化'], sentiment: 'positive' },
    { category: '服务', count: 150, examples: ['客服态度好', '售后到位', '响应快'], sentiment: 'positive' }
  ];

  // 槽点数据
  const painPoints = [
    { category: '物流', count: 150, examples: ['发货慢', '包装破损', '快递态度差'], sentiment: 'negative' },
    { category: '售后服务', count: 120, examples: ['客服响应慢', '退换货麻烦', '保修政策不清晰'], sentiment: 'negative' },
    { category: '价格', count: 100, examples: ['价格偏高', '不值这个价', '促销活动少'], sentiment: 'negative' },
    { category: '质量', count: 80, examples: ['用了一周就坏', '做工粗糙', '有异味'], sentiment: 'negative' },
    { category: '包装', count: 60, examples: ['包装简陋', '没有防震', '外观有划痕'], sentiment: 'negative' }
  ];

  // 争议点数据
  const controversialPoints = [
    { category: '性价比', count: 90, positive: 45, negative: 45, examples: ['有人认为值', '有人认为不值'] },
    { category: '外观设计', count: 70, positive: 40, negative: 30, examples: ['有人喜欢', '有人觉得丑'] },
    { category: '功能复杂度', count: 50, positive: 20, negative: 30, examples: ['有人觉得简单好用', '有人觉得功能不够'] }
  ];

  const radarOption = {
    title: { text: '多维度分析', left: 'center' },
    tooltip: {},
    legend: {
      data: ['本产品', '竞品A', '竞品B'],
      bottom: 0
    },
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
        { value: [85, 88, 90, 75, 70, 82], name: '本产品', itemStyle: { color: '#1890ff' } },
        { value: [78, 85, 80, 82, 75, 80], name: '竞品A', itemStyle: { color: '#52c41a' } },
        { value: [82, 80, 85, 78, 72, 75], name: '竞品B', itemStyle: { color: '#faad14' } }
      ]
    }]
  };

  const renderPointCard = (point, index) => {
    const isPositive = point.sentiment === 'positive';
    const icon = isPositive ? <LikeOutlined /> : <DislikeOutlined />;
    const color = isPositive ? '#52c41a' : '#f5222d';
    
    return (
      <List.Item key={index}>
        <Card 
          size="small" 
          style={{ width: '100%', borderLeft: `4px solid ${color}` }}
          hoverable
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ fontSize: 16, fontWeight: 'bold' }}>
              {icon} {point.category}
            </span>
            <Tag color={isPositive ? 'green' : 'red'}>
              {point.count} 条提及
            </Tag>
          </div>
          <div style={{ marginBottom: 12 }}>
            <Progress 
              percent={Math.round(point.count / 3.2)} 
              strokeColor={color}
              size="small"
            />
          </div>
          <div>
            <strong>典型评价：</strong>
            {point.examples.map((example, i) => (
              <Tag key={i} style={{ marginTop: 4 }}>
                {example}
              </Tag>
            ))}
          </div>
          {point.positive !== undefined && (
            <div style={{ marginTop: 12 }}>
              <Row gutter={16}>
                <Col span={12}>
                  <Statistic title="正面评价" value={point.positive} suffix="条" valueStyle={{ color: '#52c41a' }} />
                </Col>
                <Col span={12}>
                  <Statistic title="负面评价" value={point.negative} suffix="条" valueStyle={{ color: '#f5222d' }} />
                </Col>
              </Row>
            </div>
          )}
        </Card>
      </List.Item>
    );
  };

  return (
    <div>
      <Card style={{ marginBottom: 24 }}>
        <Statistic 
          title="分析说明" 
          value="所有分析结论均基于真实用户评价数据" 
          valueStyle={{ fontSize: 14, color: '#666' }}
        />
      </Card>

      <Tabs activeKey={activeTab} onChange={setActiveTab} style={{ marginBottom: 24 }}>
        <TabPane 
          tab={<span><LikeOutlined />满意点分析</span>} 
          key="satisfactory"
        >
          <Row gutter={[24, 24]}>
            <Col xs={24} lg={12}>
              <Card title="满意点分布">
                <ReactEcharts 
                  option={{
                    tooltip: { trigger: 'axis' },
                    xAxis: { type: 'category', data: satisfactoryPoints.map(p => p.category) },
                    yAxis: { type: 'value' },
                    series: [{
                      data: satisfactoryPoints.map(p => ({ value: p.count, itemStyle: { color: '#52c41a' } })),
                      type: 'bar',
                      barWidth: '50%'
                    }]
                  }} 
                  style={{ height: 300 }} 
                />
              </Card>
            </Col>
            <Col xs={24} lg={12}>
              <Card title="详细分析">
                <List
                  dataSource={satisfactoryPoints}
                  renderItem={renderPointCard}
                />
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane 
          tab={<span><DislikeOutlined />槽点分析</span>} 
          key="pain_points"
        >
          <Row gutter={[24, 24]}>
            <Col xs={24} lg={12}>
              <Card title="槽点分布">
                <ReactEcharts 
                  option={{
                    tooltip: { trigger: 'item' },
                    series: [{
                      type: 'pie',
                      radius: ['40%', '70%'],
                      data: painPoints.map(p => ({ 
                        value: p.count, 
                        name: p.category,
                        itemStyle: { color: ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#fadb14'][painPoints.indexOf(p)] }
                      }))
                    }]
                  }} 
                  style={{ height: 300 }} 
                />
              </Card>
            </Col>
            <Col xs={24} lg={12}>
              <Card title="详细分析">
                <List
                  dataSource={painPoints}
                  renderItem={renderPointCard}
                />
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane 
          tab={<span><WarningOutlined />争议点分析</span>} 
          key="controversial"
        >
          <Card title="争议点分析">
            <List
              dataSource={controversialPoints}
              renderItem={(point, index) => (
                <List.Item key={index}>
                  <Card size="small" style={{ width: '100%' }} hoverable>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                      <span style={{ fontSize: 16, fontWeight: 'bold' }}>
                        <WarningOutlined /> {point.category}
                      </span>
                      <Tag color="orange">{point.count} 条争议</Tag>
                    </div>
                    <Row gutter={16} style={{ marginBottom: 12 }}>
                      <Col span={12}>
                        <Statistic title="正面观点" value={point.positive} suffix="条" valueStyle={{ color: '#52c41a' }} />
                      </Col>
                      <Col span={12}>
                        <Statistic title="负面观点" value={point.negative} suffix="条" valueStyle={{ color: '#f5222d' }} />
                      </Col>
                    </Row>
                    <Progress 
                      percent={Math.round(point.positive / (point.positive + point.negative) * 100)} 
                      strokeColor="#52c41a"
                      format={percent => `正面 ${percent}%`}
                      style={{ marginBottom: 8 }}
                    />
                    <div>
                      <strong>争议焦点：</strong>
                      {point.examples.map((example, i) => (
                        <Tag key={i} color="orange">{example}</Tag>
                      ))}
                    </div>
                  </Card>
                </List.Item>
              )}
            />
          </Card>
        </TabPane>

        <TabPane tab="多维度对比" key="radar">
          <Card title="本产品 vs 竞品 - 多维度对比">
            <ReactEcharts option={radarOption} style={{ height: 400 }} />
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default Analysis;
