import React, { useState, useEffect } from 'react';
import pg from 'pg';

function DatabaseConnection() {
  const fetchData = async () => {
    const { Pool } = pg;
    const pool = new Pool({
      user: 'postgres',
      host: 'localhost',
      database: 'postgres',
      password: '0000',
      port: 5432, // 默认 PostgreSQL 端口
    });

    try {
      const result = await pool.query('SELECT * FROM your_table');
      setData(result.rows);
      pool.end();
    } catch (error) {
      console.error('Error executing query', error);
    }
  };
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
