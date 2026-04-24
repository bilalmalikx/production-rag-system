import { Component, EventEmitter, Output, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DragDropDirective } from '../../directives/drag-drop';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule, DragDropDirective],
  template: `
    <div class="upload-section">
      <div class="section-label">01 — Upload Document</div>
      <div class="drop-zone" appDragDrop (fileDropped)="onFileDropped.emit($event)">
        <span class="upload-icon">📂</span>
        <h3>Drop your PDF here</h3>
        <p>Drag &amp; drop or browse to select a PDF file (max 50MB)</p>
        <button class="browse-btn" (click)="fileInput.click()">
          <span>Browse Files</span>
          <span>↗</span>
        </button>
        <input #fileInput type="file" accept=".pdf" (change)="onFileSelected.emit($event)" style="display: none">
      </div>

      <!-- Upload Progress -->
      <div class="upload-progress" [class.visible]="isUploading">
        <div class="progress-card">
          <div class="progress-icon">📄</div>
          <div class="progress-info">
            <div class="progress-name">Uploading PDF...</div>
            <div class="progress-bar-track">
              <div class="progress-bar-fill" [style.width.%]="uploadProgress"></div>
            </div>
            <div class="progress-meta">
              <span>{{ uploadProgress < 30 ? 'Uploading…' : uploadProgress < 70 ? 'Processing…' : 'Building vectors…' }}</span>
              <span>{{ uploadProgress }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Upload Error -->
      <div class="error-toast" [class.visible]="uploadError">
        <span>⚠</span>
        <span>{{ uploadError }}</span>
      </div>
    </div>
  `,
  styles: [`
    .upload-section { margin-bottom: 28px; }
    .section-label { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-dim); font-weight: 600; margin-bottom: 12px; }
    .drop-zone { border: 2px dashed var(--border-bright); border-radius: var(--radius); padding: 52px 32px; text-align: center; cursor: pointer; transition: all 0.3s ease; background: var(--surface); position: relative; overflow: hidden; }
    .drop-zone.drag-over { border-color: var(--accent); background: rgba(108,99,255,0.05); transform: translateY(-2px); }
    .upload-icon { font-size: 48px; margin-bottom: 16px; display: block; animation: float 3s ease-in-out infinite; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .drop-zone h3 { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; margin-bottom: 8px; }
    .drop-zone p { color: var(--text-muted); font-size: 14px; margin-bottom: 20px; }
    .browse-btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 100px; background: linear-gradient(135deg, var(--accent), #8b5cf6); color: white; font-weight: 500; font-size: 14px; border: none; cursor: pointer; transition: all 0.25s ease; }
    .upload-progress { margin-top: 20px; display: none; animation: fadeUp 0.4s ease both; }
    .upload-progress.visible { display: block; }
    .progress-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 18px 20px; display: flex; align-items: center; gap: 16px; }
    .progress-bar-track { height: 4px; background: rgba(255,255,255,0.07); border-radius: 100px; overflow: hidden; }
    .progress-bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--teal)); border-radius: 100px; width: 0%; transition: width 0.4s ease; }
    .error-toast { display: none; align-items: center; gap: 12px; padding: 14px 18px; border-radius: var(--radius-sm); background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.25); color: var(--error); font-size: 14px; margin-top: 16px; }
    .error-toast.visible { display: flex; }
  `]
})
export class FileUploadComponent {
  @Input() isUploading = false;
  @Input() uploadProgress = 0;
  @Input() uploadError: string | null = null;
  @Output() onFileSelected = new EventEmitter<Event>();
  @Output() onFileDropped = new EventEmitter<File>();
}