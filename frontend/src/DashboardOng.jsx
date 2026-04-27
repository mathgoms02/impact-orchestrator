import { useState } from "react";
import axios from "axios";

function DashboardOng() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);

  const buscarMatches = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/matches-ong/",
      );
      setDados(response.data);
    } catch (error) {
      alert("Erro ao buscar inteligência artificial.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: "20px" }}>
      <div className="card-header">
        <h2 style={{ color: "#0f62fe" }}>Inteligência de Orquestração</h2>
        <p>
          A IA analisa as habilidades dos voluntários cadastrados e cruza com a
          sua última crise registrada.
        </p>
      </div>

      <button
        className="btn btn-primary"
        onClick={buscarMatches}
        disabled={loading}
      >
        {loading ? "Analisando perfis (IA)..." : "Encontrar Voluntários Ideais"}
      </button>

      {dados && dados.matches && (
        <div style={{ marginTop: "24px", display: "grid", gap: "16px" }}>
          <h3 style={{ fontSize: "16px" }}>Análise para: {dados.crise}</h3>

          {dados.matches.map((match, index) => (
            <div
              key={index}
              style={{
                padding: "16px",
                border: "1px solid #c6c6c6",
                borderRadius: "8px",
                background: "#f4f7f6",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "8px",
                }}
              >
                <strong style={{ fontSize: "18px" }}>{match.nome}</strong>
                <span
                  className="tag-perfil"
                  style={{ background: "#198038", color: "#fff" }}
                >
                  Aderência: {match.score_match}
                </span>
              </div>
              <p style={{ fontSize: "14px", color: "#393939" }}>
                <strong>Parecer da IA:</strong> {match.justificativa_ia}
              </p>

              <button
                className="btn btn-outline"
                style={{
                  marginTop: "12px",
                  padding: "6px 12px",
                  fontSize: "12px",
                }}
              >
                Acionar Voluntário (Agente)
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DashboardOng;
