import { useState } from "react";
import axios from "axios";

function DashboardVoluntario() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);

  const buscarOportunidades = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/matches-voluntario/",
      );
      setDados(response.data);
    } catch (error) {
      alert("Erro ao conectar com a IA.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: "20px" }}>
      <div className="card-header">
        <h2 style={{ color: "#198038" }}>Onde Precisam de Você</h2>
        <p>
          A IA cruza suas habilidades com as emergências ativas para encontrar
          onde você será mais útil.
        </p>
      </div>

      <button
        className="btn"
        style={{ backgroundColor: "#198038", color: "#fff" }}
        onClick={buscarOportunidades}
        disabled={loading}
      >
        {loading
          ? "Buscando emergências compatíveis..."
          : "Ver Matches de Voluntariado"}
      </button>

      {dados && dados.matches && (
        <div style={{ marginTop: "24px", display: "grid", gap: "16px" }}>
          <h3 style={{ fontSize: "16px" }}>
            Análise baseada no seu perfil ({dados.voluntario}):
          </h3>

          {dados.matches.map((match, index) => (
            <div
              key={index}
              style={{
                padding: "16px",
                border: "1px solid #c6c6c6",
                borderRadius: "8px",
                borderLeft: "4px solid #da1e28",
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
                <strong style={{ fontSize: "18px" }}>
                  {match.titulo_crise}
                </strong>
                <span
                  className="tag-perfil"
                  style={{ background: "#da1e28", color: "#fff" }}
                >
                  Match: {match.score_match}
                </span>
              </div>
              <p style={{ fontSize: "14px", color: "#393939" }}>
                <strong>Como você pode atuar:</strong> {match.como_ajudar}
              </p>

              <button
                className="btn btn-primary"
                style={{
                  marginTop: "12px",
                  padding: "6px 12px",
                  fontSize: "12px",
                }}
              >
                Confirmar Disponibilidade
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DashboardVoluntario;
