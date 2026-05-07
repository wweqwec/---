import React, { useState } from 'react';
import { Card, Table, Button, Tag, Row, Col, Modal, Form, Input, Select, message, Upload, Progress } from 'antd';
import { 
  DownloadOutlined, 
  FilePdfOutlined, 
  FileWordOutlined, 
  FileExcelOutlined,
  PlusOutlined,
  DeleteOutlined,
  EyeOutlined
} from '@ant-design/icons';
import { saveAs } from 'file-saver';

const { Option } = Select;
const { TextArea } = Input;

const Reports = () => {
  const [reports, setReports] = useState([
    {
      id: 'report_001',
      title: 'iPhone 15 Pro Max 全网评价分析',
      product: 'iPhone 15 Pro Max',
      createdAt: '2026-04-28 08:30',
      status: 'completed',
      formats: ['pdf', 'docx', 'xlsx'],
      dataSource: '京东、小红书、知乎',
      reviewCount: 1250
    },
    {
      id: 'report_002',
      title: '华为Mate 60 Pro 竞品对比分析',
      product: '华为Mate 60 Pro',
      createdAt: '2026-04-27 15:20',
      status: 'completed',
      formats: ['pdf'],
      dataSource: '京东、知乎',
      reviewCount: 980
    },
    {
      id: 'report_003',
      title: '小米14 Ultra 用户满意度分析',
      product: '小米14 Ultra',
      createdAt: '2026-04-26 10:15',
      status: 'generating',
      formats: [],
      dataSource: '京东、小红书',
      reviewCount: 750
    }
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [generating, setGenerating] = useState(false);

  const columns = [
    { 
      title: '报告标题', 
      dataIndex: 'title', 
      key: 'title',
      render: (text, record) => (
        <a onClick={() => handlePreview(record)}>{text}</a>
      )
    },
    { title: '产品', dataIndex: 'product', key: 'product', width: 150 },
    { title: '数据来源', dataIndex: 'dataSource', key: 'dataSource', width: 150 },
    { 
      title: '评价数量', 
      dataIndex: 'reviewCount', 
      key: 'reviewCount', 
      width: 100,
      sorter: (a, b) => a.reviewCount - b.reviewCount,
      render: (count) => <span>{count} 条</span>
    },
    { title: '生成时间', dataIndex: 'createdAt', key: 'createdAt', width: 150 },
    { 
      title: '状态', 
      key: 'status', 
      width: 100,
      render: (_, record) => {
        const config = {
          completed: { color: 'green', text: '已完成' },
          generating: { color: 'blue', text: '生成中' },
          failed: { color: 'red', text: '失败' }
        };
        const { color, text } = config[record.status];
        return <Tag color={color}>{text}</Tag>;
      }
    },
    { 
      title: '可用格式', 
      key: 'formats', 
      width: 150,
      render: (_, record) => (
        <span>
          {record.formats.includes('pdf') && <FilePdfOutlined style={{ color: '#ff4d4f', fontSize: 18, marginRight: 8 }} />}
          {record.formats.includes('docx') && <FileWordOutlined style={{ color: '#1890ff', fontSize: 18, marginRight: 8 }} />}
          {record.formats.includes('xlsx') && <FileExcelOutlined style={{ color: '#52c41a', fontSize: 18 }} />}
        </span>
      )
    },
    { 
      title: '操作', 
      key: 'action', 
      width: 200,
      render: (_, record) => (
        <span>
          {record.status === 'completed' && (
            <>
              <Button 
                type="link" 
                icon={<DownloadOutlined />}
                onClick={() => handleDownload(record, 'pdf')}
              >
                PDF
              </Button>
              <Button 
                type="link" 
                icon={<DownloadOutlined />}
                onClick={() => handleDownload(record, 'docx')}
              >
                Word
              </Button>
              <Button 
                type="link" 
                icon={<DownloadOutlined />}
                onClick={() => handleDownload(record, 'xlsx')}
              >
                Excel
              </Button>
            </>
          )}
          {record.status === 'generating' && (
            <Progress percent={65} size="small" style={{ width: 100 }} />
          )}
          <Button 
            type="link" 
            danger 
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record)}
          >
            删除
          </Button>
        </span>
      )
    }
  ];

  const handleDownload = (report, format) => {
    message.success(`开始下载 ${report.title}.${format}`);
    // 实际应该调用后端API下载文件
    // 这里模拟下载
    const blob = new Blob(['示例报告内容'], { type: 'application/octet-stream' });
    saveAs(blob, `${report.title}.${format}`);
  };

  const handlePreview = (report) => {
    Modal.info({
      title: report.title,
      content: (
        <div>
          <p><strong>产品：</strong>{report.product}</p>
          <p><strong>数据来源：</strong>{report.dataSource}</p>
          <p><strong>评价数量：</strong>{report.reviewCount} 条</p>
          <p><strong>生成时间：</strong>{report.createdAt}</p>
          <p><strong>可用格式：</strong>{report.formats.join(', ')}</p>
        </div>
      ),
      width: 500
    });
  };

  const handleDelete = (report) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除报告"${report.title}"吗？`,
      okText: '确认',
      cancelText: '取消',
      onOk: () => {
        setReports(reports.filter(r => r.id !== report.id));
        message.success('删除成功');
      }
    });
  };

  const handleGenerate = (values) => {
    setGenerating(true);
    setIsModalVisible(false);
    
    // 模拟生成过程
    setTimeout(() => {
      const newReport = {
        id: `report_${Date.now()}`,
        title: values.title,
        product: values.product,
        createdAt: new Date().toLocaleString('zh-CN'),
        status: 'completed',
        formats: ['pdf', 'docx', 'xlsx'],
        dataSource: '京东、小红书、知乎',
        reviewCount: 1000
      };
      setReports([newReport, ...reports]);
      setGenerating(false);
      message.success('报告生成成功！');
    }, 3000);
  };

  return (
    <div>
      <Card 
        title="报告管理" 
        extra={
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
          >
            生成新报告
          </Button>
        }
        style={{ marginBottom: 24 }}
      >
        <Table 
          columns={columns} 
          dataSource={reports} 
          rowKey="id"
          pagination={{ pageSize: 10 }}
          size="middle"
        />
      </Card>

      <Modal
        title="生成新报告"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form onFinish={handleGenerate} layout="vertical">
          <Form.Item 
            label="报告标题" 
            name="title" 
            rules={[{ required: true, message: '请输入报告标题' }]}
          >
            <Input placeholder="例如：iPhone 15 Pro Max 评价分析" />
          </Form.Item>

          <Form.Item 
            label="产品名称" 
            name="product" 
            rules={[{ required: true, message: '请输入产品名称' }]}
          >
            <Input placeholder="例如：iPhone 15 Pro Max" />
          </Form.Item>

          <Form.Item label="数据来源" name="dataSource">
            <Select mode="multiple" placeholder="选择数据来源">
              <Option value="jd">京东</Option>
              <Option value="xiaohongshu">小红书</Option>
              <Option value="zhihu">知乎</Option>
              <Option value="weibo">微博</Option>
              <Option value="douyin">抖音</Option>
            </Select>
          </Form.Item>

          <Form.Item label="分析维度" name="dimensions">
            <Select mode="multiple" placeholder="选择分析维度">
              <Option value="sentiment">情感分析</Option>
              <Option value="topics">主题分析</Option>
              <Option value="comparison">竞品对比</Option>
              <Option value="suggestions">改进建议</Option>
            </Select>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={generating}>
              开始生成
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Reports;
