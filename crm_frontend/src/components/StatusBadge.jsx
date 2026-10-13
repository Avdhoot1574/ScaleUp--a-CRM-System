export default function StatusBadge({ value }) {
  const key = String(value ?? 'UNKNOWN').toLowerCase().replaceAll('_','-');
  return <span className={`status-badge status-${key}`}>{String(value ?? '—').replaceAll('_',' ')}</span>;
}
