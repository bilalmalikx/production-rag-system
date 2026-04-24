import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Answer } from '../../../core/models/answer.model';
import { SafeHtmlPipe } from '../../pipes/safe-html-pipe';

@Component({
  selector: 'app-answer-display',
  standalone: true,
  imports: [CommonModule, SafeHtmlPipe],
  template: `
    <div class="answer-area">
      <!-- Latest Answer -->
      <div class="answer-card" *ngIf="currentAnswer">
        <div class="answer-header">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 16v-4M12 8h.01"/>
          </svg>
          <span class="answer-label">AI Answer</span>
          <div class="conf-badge">{{ currentAnswer.confidencePercent }}% confident</div>
        </div>
        <div class="answer-body" [innerHTML]="currentAnswer.content | safeHtml"></div>
        <div class="answer-sources" *ngIf="currentAnswer.hasSources">
          <div class="sources-label">Source Excerpts</div>
          <div *ngFor="let source of currentAnswer.sources" class="source-item">
            {{ source | safeHtml }}
          </div>
        </div>
      </div>

      <!-- History -->
      <div class="history" *ngIf="history.length > 0">
        <div class="divider"></div>
        <div class="section-label">Conversation History</div>
        <div *ngFor="let turn of history; trackBy: trackByIndex" class="turn">
          <div class="turn-question">
            <div class="turn-q-bubble">
              {{ turn.question.question }}
            </div>
          </div>
          <div class="answer-card compact">
            <div class="answer-body" [innerHTML]="turn.answer.content | safeHtml"></div>
            <div class="answer-sources" *ngIf="turn.answer.hasSources">
              <div class="sources-label">Sources</div>
              <div *ngFor="let source of turn.answer.sources" class="source-item">
                {{ source | slice:0:200 }}...
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .answer-area { margin-top: 24px; }
    .answer-card { border-radius: var(--radius); overflow: hidden; animation: revealCard 0.5s cubic-bezier(0.22, 1, 0.36, 1) both; }
    .answer-card.compact { margin-bottom: 16px; }
    .answer-header { background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(45,212,191,0.08)); border: 1px solid rgba(108,99,255,0.2); border-bottom: none; padding: 14px 20px; display: flex; align-items: center; gap: 10px; }
    .answer-label { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent2); font-weight: 600; }
    .conf-badge { margin-left: auto; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 100px; border: 1px solid rgba(45,212,191,0.3); color: var(--teal); background: rgba(45,212,191,0.1); }
    .answer-body { background: rgba(255,255,255,0.03); border: 1px solid rgba(108,99,255,0.2); border-top: none; border-bottom: none; padding: 20px; font-size: 15px; line-height: 1.75; color: var(--text); }
    .answer-sources { background: rgba(255,255,255,0.02); border: 1px solid rgba(108,99,255,0.2); border-top: none; padding: 16px 20px; }
    .sources-label { font-size: 11px; letter-spacing: 1px; text-transform: uppercase; color: var(--text-dim); font-weight: 600; margin-bottom: 12px; }
    .source-item { padding: 12px 14px; border-radius: var(--radius-sm); background: rgba(255,255,255,0.03); border: 1px solid var(--border); font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 8px; position: relative; overflow: hidden; }
    .source-item::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, var(--accent), var(--teal)); }
    .history { margin-top: 32px; display: flex; flex-direction: column; gap: 20px; }
    .turn { animation: slideIn 0.4s cubic-bezier(0.22, 1, 0.36, 1) both; }
    .turn-question { display: flex; justify-content: flex-end; margin-bottom: 12px; }
    .turn-q-bubble { background: linear-gradient(135deg, var(--accent), #7c3aed); padding: 12px 18px; border-radius: 16px 16px 4px 16px; font-size: 14px; max-width: 80%; line-height: 1.5; box-shadow: 0 4px 16px rgba(108,99,255,0.3); }
    .divider { height: 1px; background: var(--border); margin: 32px 0; position: relative; }
    .divider::after { content: '✦'; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); background: var(--bg); padding: 0 12px; font-size: 10px; color: var(--text-dim); }
    @keyframes revealCard { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideIn { from { opacity: 0; transform: translateX(-12px); } to { opacity: 1; transform: translateX(0); } }
  `]
})
export class AnswerDisplayComponent {
  @Input() currentAnswer: Answer | null = null;
  @Input() history: any[] = [];

  trackByIndex(index: number): number {
    return index;
  }
}