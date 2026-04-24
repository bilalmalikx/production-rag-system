import { Component, EventEmitter, Output, Input, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-question-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="qa-section">
      <div class="section-label">02 — Ask a Question</div>
      <div class="qa-box">
        <div class="qa-input-row">
          <div class="qa-input-wrap">
            <textarea #questionInput
              [(ngModel)]="questionText"
              (input)="onInput.emit($event)"
              (keydown)="onKeydown.emit($event)"
              [placeholder]="placeholder"
              rows="2"
              [disabled]="isLoading"></textarea>
          </div>
          <button class="ask-btn" (click)="onAsk.emit()" [disabled]="isLoading || !questionText.trim()">
            <span *ngIf="!isLoading">➤</span>
            <span *ngIf="isLoading" class="spinner">⟳</span>
          </button>
        </div>
        <div class="qa-hints">
          <span *ngFor="let hint of hints" class="hint-pill" (click)="onHintClick.emit(hint)">
            {{ hint }}
          </span>
        </div>
      </div>

      <!-- QA Error -->
      <div class="error-toast" [class.visible]="qaError">
        <span>⚠</span>
        <span>{{ qaError }}</span>
      </div>

      <!-- Typing Indicator -->
      <div class="typing-indicator" [class.visible]="isLoading">
        <div class="dots"><span></span><span></span><span></span></div>
        <span>AI is reading your document…</span>
      </div>
    </div>
  `,
  styles: [`
    .qa-section { animation: fadeUp 0.8s 0.3s cubic-bezier(0.22, 1, 0.36, 1) both; }
    .section-label { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-dim); font-weight: 600; margin-bottom: 12px; }
    .qa-box { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; transition: border-color 0.3s; }
    .qa-input-row { display: flex; gap: 12px; align-items: flex-end; }
    .qa-input-wrap { flex: 1; position: relative; }
    textarea { width: 100%; resize: none; background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px 16px; color: var(--text); font-family: 'DM Sans', sans-serif; font-size: 15px; line-height: 1.6; outline: none; min-height: 58px; max-height: 160px; }
    .ask-btn { width: 52px; height: 52px; border-radius: 14px; flex-shrink: 0; background: linear-gradient(135deg, var(--accent), #7c3aed); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.25s; color: white; font-size: 20px; }
    .ask-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .spinner { display: inline-block; animation: spin 0.8s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .qa-hints { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
    .hint-pill { font-size: 12px; padding: 6px 14px; border-radius: 100px; background: rgba(255,255,255,0.04); border: 1px solid var(--border); color: var(--text-muted); cursor: pointer; transition: all 0.2s; }
    .hint-pill:hover { background: rgba(108,99,255,0.1); border-color: rgba(108,99,255,0.3); color: var(--accent2); }
    .error-toast { display: none; align-items: center; gap: 12px; padding: 14px 18px; border-radius: var(--radius-sm); background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.25); color: var(--error); font-size: 14px; margin-top: 16px; }
    .error-toast.visible { display: flex; }
    .typing-indicator { display: none; padding: 20px; background: rgba(255,255,255,0.03); border: 1px solid rgba(108,99,255,0.2); border-radius: var(--radius); align-items: center; gap: 10px; color: var(--text-muted); font-size: 14px; margin-top: 20px; }
    .typing-indicator.visible { display: flex; animation: revealCard 0.3s ease both; }
    .dots { display: flex; gap: 5px; }
    .dots span { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); animation: bounce 1.2s ease-in-out infinite; }
    .dots span:nth-child(2) { animation-delay: 0.2s; }
    .dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-8px); } }
  `]
})
export class QuestionInputComponent {
  @Input() questionText = '';
  @Input() isLoading = false;
  @Input() qaError: string | null = null;
  @Input() placeholder = 'e.g. What are the key findings in section 3?';
  @Input() hints: string[] = [];
  @Output() questionTextChange = new EventEmitter<string>();
  @Output() onAsk = new EventEmitter<void>();
  @Output() onInput = new EventEmitter<Event>();
  @Output() onKeydown = new EventEmitter<KeyboardEvent>();
  @Output() onHintClick = new EventEmitter<string>();
}