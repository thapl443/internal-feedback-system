import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Home, Inbox, Trophy, Megaphone, ClipboardList, 
  Send, ShieldCheck, AlertCircle, TrendingUp, BarChart,
  Shield, Zap
} from 'lucide-react';

const API_BASE = "http://localhost:8000";

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [announcements, setAnnouncements] = useState([]);
  const [scores, setScores] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [summary, setSummary] = useState(null);
  
  // Form States
  const [complaintForm, setComplaintForm] = useState({ subject: '', description: '' });
  const [surveyForm, setSurveyForm] = useState({ topic: 'Employee Satisfaction', answer: 'Agree', comment: '' });
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      const [annRes, scoreRes, compRes, sumRes] = await Promise.all([
        axios.get(`${API_BASE}/announcements`),
        axios.get(`${API_BASE}/scores`),
        axios.get(`${API_BASE}/complaints`),
        axios.get(`${API_BASE}/analytics/summary`)
      ]);
      setAnnouncements(annRes.data);
      setScores(scoreRes.data);
      setComplaints(compRes.data);
      setSummary(sumRes.data);
    } catch (err) {
      console.error("Fetch error", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleComplaintSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/complaints`, complaintForm);
      setComplaintForm({ subject: '', description: '' });
      fetchData();
      alert("ส่งเรื่องเรียบร้อย! ระบบกำลังวิเคราะห์แนวทางแก้ไข...");
    } finally {
      setLoading(false);
    }
  };

  const renderHome = () => (
    <div className="tab-content animate-fade-in">
      <div className="section-header">
        <Megaphone size={24} color="var(--primary)" />
        <h2>ข่าวประกาศล่าสุด</h2>
      </div>
      <div className="announcement-list">
        {announcements.map(a => (
          <div key={a.id} className="glass-card mb-1">
            <h3>{a.title}</h3>
            <p>{a.content}</p>
            <span className="date">{new Date(a.created_at).toLocaleDateString('th-TH')}</span>
          </div>
        ))}
      </div>

      <div className="section-header mt-3">
        <Trophy size={24} color="#f59e0b" />
        <h2>ตารางคะแนนกีฬาสี</h2>
      </div>
      <div className="stats-grid">
        {scores.map(s => (
          <div key={s.id} className="stat-card" style={{ borderLeft: `4px solid ${s.team_color.toLowerCase()}` }}>
            <h3>สี{s.team_color === 'Red' ? 'แดง' : s.team_color === 'Blue' ? 'น้ำเงิน' : s.team_color === 'Green' ? 'เขียว' : 'เหลือง'}</h3>
            <div className="value">{s.score}</div>
            <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>อัปเดตล่าสุด: {new Date(s.last_updated).toLocaleTimeString()}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderComplaints = () => (
    <div className="tab-content animate-fade-in">
      <div className="glass-card mb-2">
        <h2 className="mb-1">ส่งเรื่องร้องเรียน / แจ้งปัญหา</h2>
        <form onSubmit={handleComplaintSubmit}>
          <input 
            type="text" 
            placeholder="หัวข้อเรื่อง (เช่น แจ้งแอร์ไม่เย็น, ลืมรหัสผ่าน)" 
            value={complaintForm.subject}
            onChange={e => setComplaintForm({...complaintForm, subject: e.target.value})}
            className="modern-input mb-1"
            required
          />
          <textarea 
            placeholder="รายละเอียดเพิ่มเติม..."
            value={complaintForm.description}
            onChange={e => setComplaintForm({...complaintForm, description: e.target.value})}
            className="modern-input mb-1"
            rows="4"
            required
          />
          <button className="btn-primary" type="submit" disabled={loading}>
            <Send size={18} /> {loading ? "กำลังส่ง..." : "ส่งเรื่อง"}
          </button>
        </form>
      </div>

      <div className="section-header mt-3">
        <ShieldCheck size={24} color="var(--success)" />
        <h2>สถานะและการวิเคราะห์ข้อมูล (Decision Support)</h2>
      </div>
      <div className="complaint-list">
        {complaints.map(c => (
          <div key={c.id} className="glass-card mb-1 complaint-item">
            <div className="item-main">
              <h3>{c.subject}</h3>
              <p>{c.description}</p>
              <div className="ai-badge-group">
                <span className="badge badge-primary">แนะแผนก: {c.suggested_department}</span>
                <span className={`badge priority-${c.priority_score > 3 ? 'high' : 'medium'}`}>ความสำคัญ: {c.priority_score}/5</span>
                <span className={`badge sentiment-${c.sentiment?.toLowerCase()}`}>Sentiment: {c.sentiment}</span>
              </div>
            </div>
            <div className="ai-recommendation">
              <h4><AlertCircle size={14} inline /> ข้อแนะนำจากระบบ:</h4>
              <p>{c.ai_recommendation}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderSurveys = () => (
    <div className="tab-content animate-fade-in">
      <div className="glass-card">
        <h2 className="mb-1">แบบสอบถามความพึงพอใจ</h2>
        <p className="mb-2">หัวข้อ: ความพึงพอใจในการทำงานประจำเดือน</p>
        <div className="survey-options mb-2">
          {['Agree', 'Neutral', 'Disagree'].map(opt => (
            <button 
              key={opt}
              className={`btn-outline ${surveyForm.answer === opt ? 'active' : ''}`}
              onClick={() => setSurveyForm({...surveyForm, answer: opt})}
            >
              {opt === 'Agree' ? '😊 เห็นด้วย' : opt === 'Neutral' ? '😐 เฉยๆ' : '☹️ ไม่เห็นด้วย'}
            </button>
          ))}
        </div>
        <textarea 
          placeholder="ความเห็นเพิ่มเติม..."
          className="modern-input mb-1"
          value={surveyForm.comment}
          onChange={e => setSurveyForm({...surveyForm, comment: e.target.value})}
        />
        <button className="btn-primary" onClick={async () => {
          try {
            await axios.post(`${API_BASE}/surveys`, surveyForm);
            alert("ขอบคุณสำหรับข้อมูลครับ!");
            setSurveyForm({ topic: 'ความพึงพอใจในการทำงานประจำเดือน', answer: 'Agree', comment: '' });
          } catch (err) {
            alert("เกิดข้อผิดพลาดในการส่งข้อมูล");
          }
        }}>ส่งแบบสอบถาม</button>
      </div>
    </div>
  );

  const [rawDb, setRawDb] = useState(null);

  const fetchRawDb = async () => {
    const res = await axios.get(`${API_BASE}/admin/raw-db`);
    setRawDb(res.data);
  };

  const runEtl = async () => {
    try {
      await axios.post(`${API_BASE}/etl/run`);
      alert("ETL Pipeline executed successfully!");
      fetchData();
    } catch (err) {
      alert("Failed to run ETL");
    }
  };

  const [newAnn, setNewAnn] = useState({ title: '', content: '' });

  const handleAddAnnouncement = async () => {
    await axios.post(`${API_BASE}/announcements`, newAnn);
    setNewAnn({ title: '', content: '' });
    fetchData(); // Refresh list
  };

  const handleDeleteAnn = async (id) => {
    await axios.delete(`${API_BASE}/announcements/${id}`);
    fetchData(); // Refresh list
  };

  const handleUpdateScore = async (id, newScore) => {
    await axios.patch(`${API_BASE}/scores/${id}?score=${newScore}`);
    fetchData();
  };

  const renderAdmin = () => (
    <div className="tab-content animate-fade-in">
       <div className="section-header">
        <Shield size={24} color="var(--primary)" />
        <h2>Admin Control Panel (Management)</h2>
      </div>
      
      <div className="grid-2">
        {/* Left: System Analytics & Sports Manager */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-card">
            <h3>System Analytics</h3>
            <div className="stats-grid" style={{ gridTemplateColumns: '1fr' }}>
              <div className="stat-card">
                <h3>Total Complaints</h3>
                <div className="value">{summary?.total_complaints || 0}</div>
              </div>
            </div>
            <button className="btn-primary mt-1 w-full" style={{ background: 'var(--success)' }} onClick={runEtl}>
              <Zap size={16} /> Run ETL Pipeline Manually
            </button>
          </div>

          <div className="glass-card">
            <h3>Sports Score Manager</h3>
            <div className="score-manager-list">
              {scores.map(s => (
                <div key={s.id} className="score-edit-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem', padding: '0.5rem', background: 'rgba(255,255,255,0.03)', borderRadius: '0.5rem' }}>
                  <span style={{ fontWeight: 600 }}>สี{s.team_color}</span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <button className="btn-outline" style={{ padding: '0.2rem 0.6rem' }} onClick={() => handleUpdateScore(s.id, s.score - 10)}>-10</button>
                    <span className="value" style={{ minWidth: '40px', textAlign: 'center', fontWeight: 'bold', color: 'var(--primary)' }}>{s.score}</span>
                    <button className="btn-outline" style={{ padding: '0.2rem 0.6rem' }} onClick={() => handleUpdateScore(s.id, s.score + 10)}>+10</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Add Announcement */}
        <div className="glass-card">
          <h3>Create New Announcement</h3>
          <input 
            className="modern-input mb-1" 
            placeholder="หัวข้อประกาศ..." 
            value={newAnn.title}
            onChange={e => setNewAnn({...newAnn, title: e.target.value})}
          />
          <textarea 
            className="modern-input mb-1" 
            placeholder="เนื้อหาประกาศ..." 
            value={newAnn.content}
            onChange={e => setNewAnn({...newAnn, content: e.target.value})}
          />
          <button className="btn-primary w-full" onClick={handleAddAnnouncement}>บันทึกประกาศ</button>
        </div>
      </div>

      <div className="glass-card mt-2">
        <h3>Manage Active Announcements</h3>
        <table className="modern-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {announcements.map(ann => (
              <tr key={ann.id}>
                <td>{ann.title}</td>
                <td>{new Date(ann.created_at).toLocaleDateString()}</td>
                <td>
                  <button className="btn-outline" style={{ color: 'var(--danger)', borderColor: 'var(--danger)' }} onClick={() => handleDeleteAnn(ann.id)}>ลบ</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="glass-card mt-2">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>Database Persistence Logs</h3>
          <button className="btn-outline" onClick={fetchRawDb}>Inspect JSON</button>
        </div>
        {rawDb && (
          <pre className="code-block mt-1" style={{ fontSize: '0.7rem', maxHeight: '200px', overflow: 'auto' }}>
            {JSON.stringify(rawDb, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-logo">Nexus Internal</div>
        <nav>
          <button className={activeTab === 'home' ? 'active' : ''} onClick={() => setActiveTab('home')}><Home size={20}/> หน้าแรก & กีฬาสี</button>
          <button className={activeTab === 'complaints' ? 'active' : ''} onClick={() => setActiveTab('complaints')}><Inbox size={20}/> กล่องรับเรื่อง</button>
          <button className={activeTab === 'surveys' ? 'active' : ''} onClick={() => setActiveTab('surveys')}><ClipboardList size={20}/> แบบสอบถาม</button>
          <button className={activeTab === 'admin' ? 'active' : ''} onClick={() => setActiveTab('admin')}><TrendingUp size={20}/> วิเคราะห์สรุปผล</button>
        </nav>
      </aside>
      
      <main className="content">
        {activeTab === 'home' && renderHome()}
        {activeTab === 'complaints' && renderComplaints()}
        {activeTab === 'surveys' && renderSurveys()}
        {activeTab === 'admin' && renderAdmin()}
      </main>
    </div>
  );
}

export default App;
