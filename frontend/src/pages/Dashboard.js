import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Progress, Spin, Alert } from 'antd';
import { 
  ArrowUpOutlined, 
  ArrowDownOutlined, 
  CommentOutlined, 
  LikeOutlined, 
  DislikeOutlined, 
  MehOutlined 
} from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import axios from 'axios';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    // 模拟数据加载
    setTimeout(() => {
      setData({
        totalReviews: 1000,
        sentiment: { positive: 450, neutral: 300, negative: 250 },
        platforms: [
          { name: '京东', count: 450, percentage: 45 },
          { name: '小红书', count: 280, percentage: 28 },
          { name: '知乎', count: 170, percentage: 17 },
          { name: '其他', count: 100, percentage: 10 }
        ],
        recentReviews: [
          { id: 1, source: '京东', author: '张*', content: '这个产品真的很不错，性价比很高，推荐购买！', rating: 5, sentiment: 'positive', date: '2026-04-28' },
          { id: 2, source: '小红书', author: '小***', content: '外观很好看，但是物流有点慢', rating: 4, sentiment: 'neutral', date: '2026-04-27' },
          { id: 3, source: '京东', author: '李*', content: '质量不行，用了两周就坏了', rating: 2, sentiment: 'negative', date: '2026-04-26' },
          { id: 4, source: '知乎', author: '王**', content: '对比了几款产品，这款性价比最高', rating: 5, sentiment: 'positive', date: '2026-04-25' },
          { id: 5, source: '小红书', author: '美***', content: '客服态度很差，退货麻烦', rating: 1, sentiment: 'negative', date: '2026-04-24' }
        ]
      });
      setLoading(false);
    }, 1000);
  }, []);

  const sentimentPieOption = {
    title: { text: '情感分布', left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [
      {
        name: '情感分布',
        type: 'pie',
        radius: '50%',
        data: [
          { value: data?.sentiment.positive || 0, name: '正面', itemStyle: { color: '#52c41a' } },
          { value: data?.sentiment.neutral || 0, name: '中性', itemStyle: { color: '#faad14' } },
          { value: data?.sentiment.negative || 0, name: '负面', itemStyle: { color: '#f5222d' } }
        ],
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
        }
      }
    ]
  };

  const platformBarOption = {
    title: { text: '数据来源分布', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: data?.platforms.map(p => p.name) || [] },
    yAxis: { type: 'value' },
    series: [
      {
        data: data?.platforms.map(p => ({ value: p.count, itemStyle: { color: '#1890ff' } })) || [],
        type: 'bar',
        barWidth: '50%'
      }
    ]
  };

  const columns = [
    { title: '来源', dataIndex: 'source', key: 'source', width: 100 },
    { title: '用户', dataIndex: 'author', key: 'author', width: 100 },
    { title: '评价内容', dataIndex: 'content', key: 'content', ellipsis: true },
    { 
      title: '评分', 
      dataIndex: 'rating', 
      key: 'rating', 
      width: 80,
      render: (rating) => <span style={{ color: rating >= 4 ? '#52c41a' : rating >= 3 ? '#faad14' : '#f5222d' }}>{rating}★</span>
    },
    { 
      title: '情感', 
      dataIndex: 'sentiment', 
      key: 'sentiment', 
      width: 80,
      render: (sentiment) => {
        const config = {
          positive: { color: 'green', text: '正面', icon: <LikeOutlined /> },
          neutral: { color: 'orange', text: '中性', icon: <MehOutlined /> },
          negative: { color: 'red', text: '负面', icon: <DislikeOutlined /> }
        };
        const { color, text, icon } = config[sentiment];
        return <Tag color={color} icon={icon}>{text}</Tag>;
      }
    },
    { title: '日期', dataIndex: 'date', key: 'date', width: 120 }
  ];

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }} />;
  }

  return (
    <div>
      <Alert
        message="数据更新提醒"
        description="最近一次数据更新时间为 2026-04-28 08:30，共采集 1000 条评价数据。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Row gutter={[24, 24]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={6}>
          <Card hoverable>
            <Statistic
              title="评价总数"
              value={data.totalReviews}
              prefix={<CommentOutlined style={{ color: '#1890ff' }} />}
              suffix="条"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card hoverable>
            <Statistic
              title="正面评价"
              value={data.sentiment.positive}
              valueStyle={{ color: '#52c41a' }}
              prefix={<LikeOutlined />}
              suffix="条"
            />
            <div style={{ marginTop: 8 }}>
              <Progress percent={45} strokeColor="#52c41a" size="small" />
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card hoverable>
            <Statistic
              title="中性评价"
              value={data.sentiment.neutral}
              valueStyle={{ color: '#faad14' }}
              prefix={<MehOutlined />}
              suffix="条"
            />
            <div style={{ marginTop: 8 }}>
              <Progress percent={30} strokeColor="#faad14" size="small" />
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card hoverable>
            <Statistic
              title="负面评价"
              value={data.sentiment.negative}
              valueStyle={{ color: '#f5222d' }}
              prefix={<DislikeOutlined />}
              suffix="条"
            />
            <div style={{ marginTop: 8 }}>
              <Progress percent={25} strokeColor="#f5222d" size="small" />
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[24, 24]} style={{ marginBottom: 24 }}>
        <Col xs={24} md={12}>
          <Card title="情感分布">
            <ReactECharts option={sentimentPieOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card title="数据来源分布">
            <ReactECharts option={platformBarOption} style={{ height: 300 }} />
          </Card>
        </Col>
      </Row>

      <Card title="最近评价">
        <Table 
          columns={columns} 
          dataSource={data.recentReviews} 
          rowKey="id" 
          pagination={{ pageSize: 5 }}
          size="middle"
        />
      </Card>
    </div>
  );
};

export default Dashboard;
