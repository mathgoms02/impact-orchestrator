import { useState, useEffect } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import RegistroVoluntario from "./RegistroVoluntario";
import RegistroCrise from "./RegistroCrise";
import "./App.css";
import logo from "./assets/logo.png";
import DashboardOng from "./DashboardOng";
import DashboardVoluntario from "./DashboardVoluntario";

const API_URL = "http://127.0.0.1:8000/api";

function App() {
  const [user, setUser] = useState(null);
  const [modoCadastro, setModoCadastro] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    tipo: "VOLUNTARIO",
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) setUser(jwtDecode(token));
  }, []);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const fazerLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_URL}/login/`, {
        username: formData.username,
        password: formData.password,
      });
      localStorage.setItem("access_token", res.data.access);
      setUser(jwtDecode(res.data.access));
    } catch (error) {
      alert("Erro no login. Verifique as credenciais.");
    }
  };

  const fazerCadastro = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/cadastro/`, formData);
      alert("Conta criada! Faça login para continuar.");
      setModoCadastro(false);
    } catch (error) {
      alert("Erro ao cadastrar.");
    }
  };

  const sair = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  // TELA DE AUTENTICAÇÃO
  if (!user) {
    return (
      <div className="auth-container">
        <div className="card card-auth">
          <div className="logo">
            <img src={logo} alt="" />
          </div>
          <div className="card-header">
            <h2>{modoCadastro ? "Criar Nova Conta" : "Impact Orchestrator"}</h2>
            <p>
              {modoCadastro
                ? "Junte-se à rede de impacto social com Impact Orchestrator."
                : "Insira suas credenciais para continuar."}
            </p>
          </div>

          <form
            onSubmit={modoCadastro ? fazerCadastro : fazerLogin}
            className="form-grid"
          >
            <div className="input-group span-2">
              <label>Nome de Usuário</label>
              <input
                type="text"
                name="username"
                placeholder="Digite seu username..."
                required
                onChange={handleChange}
              />
            </div>

            {modoCadastro && (
              <>
                <div className="input-group span-2">
                  <label>E-mail</label>
                  <input
                    type="email"
                    name="email"
                    placeholder="Digite seu e-mail..."
                    required
                    onChange={handleChange}
                  />
                </div>
                <div className="input-group span-2">
                  <label>Tipo de Perfil</label>
                  <select
                    name="tipo"
                    value={formData.tipo}
                    onChange={handleChange}
                  >
                    <option value="VOLUNTARIO">Sou Voluntário</option>
                    <option value="ONG">Sou Instituição / ONG</option>
                  </select>
                </div>
              </>
            )}

            <div className="input-group span-2">
              <label>Senha</label>
              <input
                type="password"
                name="password"
                placeholder="Digite sua senha..."
                required
                onChange={handleChange}
              />
            </div>

            <button className="btn btn-primary span-2" type="submit">
              {modoCadastro ? "Finalizar Cadastro" : "Entrar na Plataforma"}
            </button>

            <span
              className="text-link span-2"
              onClick={() => setModoCadastro(!modoCadastro)}
            >
              {modoCadastro
                ? "Já tem conta? Entrar agora"
                : "Novo por aqui? Cadastre-se"}
            </span>
          </form>
        </div>
      </div>
    );
  }

  // TELA LOGADA
  return (
    <div className="app-wrapper">
      <nav className="nav-bar">
        <div>
          <strong style={{ fontSize: "18px", marginRight: "12px" }}>
            Impact Orchestrator | {user.username}
          </strong>
          <span
            className={
              user.tipo === "ONG" ? "tag-perfil tag-ong" : "tag-perfil"
            }
          >
            {user.tipo === "ONG" ? "Instituição" : "Voluntário"}
          </span>
        </div>
        <button onClick={sair} className="btn btn-outline">
          Sair
        </button>
      </nav>

      <main className="main-content">
        {user.tipo === "VOLUNTARIO" ? (
          <>
            <RegistroVoluntario />
            <DashboardVoluntario /> {/* <-- Inserido aqui! */}
          </>
        ) : (
          <>
            <RegistroCrise />
            <DashboardOng /> {/* <-- Inserido aqui! */}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
