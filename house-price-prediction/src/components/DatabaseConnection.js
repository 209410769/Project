import React, { useState, useEffect } from 'react';
import { Pool } from 'pg';

function DatabaseConnection() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const pool = new Pool({
        user: 'postgres',
        host: 'localhost',
        database: 'postgres', // 替换为你的数据库名
        password: '0000',
        port: 5432, // 默认 PostgreSQL 端口
      });

      try {
        const result = await pool.query('SELECT * FROM your_table'); // 替换为你的表名
        setData(result.rows);
        pool.end();
      } catch (error) {
        console.error('Error executing query', error);
      }
    };

    fetchData();

    // 组件卸载时清理资源
    return () => {
      // 清理操作，例如取消未完成的请求或断开数据库连接
    };
  }, []); // 传递空数组作为第二个参数，确保 useEffect 只在组件挂载和卸载时执行

  return (
    <div>
      <h1>Data from PostgreSQL:</h1>
      <ul>
        {data.map((item, index) => (
          <li key={index}>{item.column_name}</li>
          // 替换 'column_name' 为数据库中实际的列名
        ))}
      </ul>
    </div>
  );
}

export default DatabaseConnection;
