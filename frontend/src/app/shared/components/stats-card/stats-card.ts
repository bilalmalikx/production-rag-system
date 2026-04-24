import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stats-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-val accent">{{ stats.documents }}</div>
        <div class="stat-lbl">Documents Loaded</div>
      </div>
      <div class="stat-card">
        <div class="stat-val teal">{{ stats.questions }}</div>
        <div class="stat-lbl">Questions Asked</div>
      </div>
      <div class="stat-card">
        <div class="stat-val success">{{ stats.avgConfidence }}%</div>
        <div class="stat-lbl">Avg Confidence</div>
      </div>
    </div>
  `,
  styles: [`
    .stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 32px; animation: fadeUp 0.8s 0.15s cubic-bezier(0.22, 1, 0.36, 1) both; }
    .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 18px; text-align: center; transition: all 0.3s; }
    .stat-card:hover { background: var(--surface-hover); transform: translateY(-2px); }
    .stat-val { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; margin-bottom: 4px; }
    .stat-val.accent { color: var(--accent2); }
    .stat-val.teal { color: var(--teal); }
    .stat-val.success { color: var(--success); }
    .stat-lbl { font-size: 12px; color: var(--text-dim); font-weight: 500; letter-spacing: 0.5px; }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class StatsCardComponent {
  @Input() stats = { documents: 0, questions: 0, avgConfidence: 0 };
}