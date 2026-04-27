import { useState, useEffect } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import RegistroVoluntario from "./RegistroVoluntario";
import RegistroCrise from "./RegistroCrise";
import "./GridForms.css";

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
      alert("Conta criada! Faça login.");
      setModoCadastro(false);
    } catch (error) {
      alert("Erro ao cadastrar.");
    }
  };

  const sair = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  if (!user) {
    return (
      <div
        className="form-container"
        style={{ maxWidth: "400px", margin: "50px auto" }}
      >
        <h2>{modoCadastro ? "Criar Conta" : "Entrar"}</h2>
        <form
          onSubmit={modoCadastro ? fazerCadastro : fazerLogin}
          className="formulario-grid"
        >
          <input
            className="grid-span-2"
            type="text"
            name="username"
            placeholder="Usuário"
            required
            onChange={handleChange}
          />
          {modoCadastro && (
            <>
              <input
                className="grid-span-2"
                type="email"
                name="email"
                placeholder="E-mail"
                required
                onChange={handleChange}
              />
              <select
                className="grid-span-2"
                name="tipo"
                value={formData.tipo}
                onChange={handleChange}
                style={{ padding: "12px" }}
              >
                <option value="VOLUNTARIO">Voluntário</option>
                <option value="ONG">Instituição</option>
              </select>
            </>
          )}
          <input
            className="grid-span-2"
            type="password"
            name="password"
            placeholder="Senha"
            required
            onChange={handleChange}
          />
          <button className="btn-submit grid-span-2" type="submit">
            {modoCadastro ? "Cadastrar" : "Entrar"}
          </button>
        </form>
        <p
          style={{ marginTop: "15px", color: "#0f62fe", cursor: "pointer" }}
          onClick={() => setModoCadastro(!modoCadastro)}
        >
          {modoCadastro ? "Já tem conta? Entrar" : "Novo por aqui? Cadastre-se"}
        </p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: "1000px", margin: "20px auto", padding: "20px" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          background: "#fff",
          padding: "15px",
          borderRadius: "8px",
          marginBottom: "20px",
        }}
      >
        <div>
          <h2 style={{ margin: 0 }}>Olá, {user.username}</h2>
          <span style={{ color: "#da1e28" }}>Perfil: {user.tipo}</span>
        </div>
        <button
          onClick={sair}
          className="btn-submit"
          style={{ background: "#393939" }}
        >
          Sair
        </button>
      </header>

      {user.tipo === "VOLUNTARIO" ? (
        <>
          <RegistroVoluntario />
          <div className="form-container">
            <h3>Em breve: Mural de Crises para você ajudar</h3>
          </div>
        </>
      ) : (
        <>
          <RegistroCrise />
          <div className="form-container">
            <h3>Em breve: Dashboard de Matches e IA</h3>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
