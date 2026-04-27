import { useState } from "react";
import axios from "axios";

function RegistroCrise() {
  const [crise, setCrise] = useState({ titulo: "", descricao_bruta: "" });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post("http://127.0.0.1:8000/api/crises/", crise);
      alert(
        "Alerta emitido! O watsonx está processando as habilidades necessárias.",
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 style={{ color: "#da1e28" }}>Emitir Alerta de Crise</h2>
        <p>
          Descreva o cenário. A IA da IBM se encarregará de estruturar as
          necessidades.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="form-grid">
        <div className="input-group span-2">
          <label>Título da Emergência</label>
          <input
            type="text"
            placeholder="Ex: Deslizamento no Bairro Central"
            required
            onChange={(e) => setCrise({ ...crise, titulo: e.target.value })}
          />
        </div>

        <div className="input-group span-2">
          <label>Descrição Completa do Cenário</label>
          <textarea
            rows="4"
            placeholder="Fale em linguagem natural o que aconteceu e de quem você precisa agora..."
            required
            onChange={(e) =>
              setCrise({ ...crise, descricao_bruta: e.target.value })
            }
          />
        </div>

        <button
          type="submit"
          className="btn btn-danger span-2"
          disabled={loading}
        >
          {loading
            ? "Orquestrando com watsonx..."
            : "Disparar Alerta e Buscar Voluntários"}
        </button>
      </form>
    </div>
  );
}
export default RegistroCrise;
