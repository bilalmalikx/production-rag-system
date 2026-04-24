import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil, debounceTime } from 'rxjs';

// Models
import { Document } from '../../core/models/document.model';
import { Answer } from '../../core/models/answer.model';
import { DragDropDirective } from '../../shared/directives/drag-drop';
import { SafeHtmlPipe } from '../../shared/pipes/safe-html-pipe';
import { ApiService } from '../../core/services/api';
import { DocumentService } from '../../core/services/document';
import { QuestionService } from '../../core/services/question';
import { FileUploadComponent } from '../../shared/components/file-upload/file-upload';
import { QuestionInputComponent } from '../../shared/components/question-input/question-input';
import { AnswerDisplayComponent } from '../../shared/components/answer-display/answer-display';
import { StatsCardComponent } from '../../shared/components/stats-card/stats-card';

// Services

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    DragDropDirective, 
    SafeHtmlPipe,
    FileUploadComponent,
    QuestionInputComponent,
    AnswerDisplayComponent,
    StatsCardComponent   
  ],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent implements OnInit, OnDestroy {
  @ViewChild('questionInput') questionInput!: ElementRef<HTMLTextAreaElement>;
  
  // State variables
  documents: Document[] = [];
  selectedDocument: Document | null = null;
  currentAnswer: Answer | null = null;
  history: any[] = [];
  isLoading = false;
  uploadProgress = 0;
  isUploading = false;
  uploadError: string | null = null;
  qaError: string | null = null;
  
  // Form
  questionText = '';
  hints = [
    'Summarize the document',
    'What are the main conclusions?',
    'List key statistics mentioned',
    'Who are the authors?'
  ];
  
  // Stats
  stats = {
    documents: 0,
    questions: 0,
    avgConfidence: 0
  };
  
  private destroy$ = new Subject<void>();

  constructor(
    private apiService: ApiService,
    private documentService: DocumentService,
    private questionService: QuestionService
  ) {}

  ngOnInit(): void {
    // Subscribe to documents
    this.documentService.documents$
      .pipe(takeUntil(this.destroy$))
      .subscribe(docs => {
        this.documents = docs;
        this.stats.documents = docs.length;
      });
    
    // Subscribe to selected document
    this.documentService.selectedDocument$
      .pipe(takeUntil(this.destroy$))
      .subscribe(doc => {
        this.selectedDocument = doc;
      });
    
    // Subscribe to current answer
    this.questionService.currentAnswer$
      .pipe(takeUntil(this.destroy$))
      .subscribe(answer => {
        this.currentAnswer = answer;
      });
    
    // Subscribe to history
    this.questionService.history$
      .pipe(takeUntil(this.destroy$))
      .subscribe(history => {
        this.history = history;
      });
    
    // Subscribe to loading state
    this.questionService.isLoading$
      .pipe(takeUntil(this.destroy$))
      .subscribe(loading => {
        this.isLoading = loading;
      });
    
    // Subscribe to upload progress
    this.documentService.uploadProgress$
      .pipe(takeUntil(this.destroy$), debounceTime(50))
      .subscribe(progress => {
        this.uploadProgress = progress;
      });
    
    // Subscribe to question count
    this.questionService.questionCount$
      .pipe(takeUntil(this.destroy$))
      .subscribe(count => {
        this.stats.questions = count;
        this.updateAvgConfidence();
      });
    
    // Subscribe to confidence scores
    this.questionService.confidenceScores$
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.updateAvgConfidence();
      });
    
    // Check backend health
    this.checkHealth();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  updateAvgConfidence(): void {
    this.stats.avgConfidence = Math.round(this.questionService.getAverageConfidence() * 100);
  }

  checkHealth(): void {
    this.apiService.checkHealth().subscribe({
      next: () => console.log('Backend healthy'),
      error: (err) => console.warn('Backend not responding:', err.message)
    });
  }

  // File handling
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.uploadFile(input.files[0]);
    }
  }

  onFileDropped(file: File): void {
    this.uploadFile(file);
  }

  uploadFile(file: File): void {
    if (!file.name.endsWith('.pdf')) {
      this.showUploadError('Only PDF files are supported.');
      return;
    }
    
    if (file.size > 50 * 1024 * 1024) {
      this.showUploadError('File too large. Maximum size is 50MB.');
      return;
    }
    
    this.isUploading = true;
    this.uploadError = null;
    this.documentService.resetUploadProgress();
    
    // Simulate progress animation
    this.animateProgress(0, 30, 400);
    
    this.apiService.uploadPDF(file).subscribe({
      next: (response) => {
        this.animateProgress(70, 100, 500);
        
        setTimeout(() => {
          const document = new Document(
            response.filename,
            response.pages,
            response.chunks
          );
          this.documentService.addDocument(document);
          this.isUploading = false;
          this.documentService.resetUploadProgress();
        }, 500);
      },
      error: (err) => {
        this.isUploading = false;
        this.documentService.resetUploadProgress();
        this.showUploadError(err.message);
      }
    });
  }

  animateProgress(from: number, to: number, duration: number): void {
    const startTime = performance.now();
    const step = (now: number) => {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      const value = Math.round(from + (to - from) * t);
      this.documentService.setUploadProgress(value);
      if (t < 1) {
        requestAnimationFrame(step);
      }
    };
    requestAnimationFrame(step);
  }

  showUploadError(message: string): void {
    this.uploadError = message;
    setTimeout(() => {
      this.uploadError = null;
    }, 5000);
  }

  // Question handling
  askQuestion(): void {
    if (!this.questionText.trim()) return;
    if (!this.selectedDocument && this.documents.length === 0) {
      this.showQAError('Please upload a document first.');
      return;
    }
    
    this.qaError = null;
    this.questionService.setLoading(true);
    
    const request = {
      question: this.questionText.trim(),
      pdf_name: this.selectedDocument?.name || this.documents[0]?.name
    };
    
    this.apiService.askQuestion(request).subscribe({
      next: (response) => {
        const answer = new Answer(
          response.question,
          response.answer,
          response.confidence,
          response.source_chunks
        );
        
        this.questionService.addToHistory(this.questionText, answer);
        this.questionService.setCurrentAnswer(answer);
        this.questionService.setLoading(false);
        
        // Clear input
        this.questionText = '';
        this.resetTextareaHeight();
      },
      error: (err) => {
        this.questionService.setLoading(false);
        this.showQAError(err.message);
      }
    });
  }

  showQAError(message: string): void {
    this.qaError = message;
    setTimeout(() => {
      this.qaError = null;
    }, 5000);
  }

  selectDocument(document: Document): void {
    this.documentService.selectDocument(document);
  }

  fillHint(hint: string): void {
    this.questionText = hint;
    this.focusTextarea();
  }

  focusTextarea(): void {
    setTimeout(() => {
      this.questionInput?.nativeElement.focus();
    });
  }

  resetTextareaHeight(): void {
    setTimeout(() => {
      if (this.questionInput) {
        this.questionInput.nativeElement.style.height = 'auto';
      }
    });
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.askQuestion();
    }
  }

  autoResizeTextarea(event: Event): void {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px';
  }

  trackByIndex(index: number): number {
    return index;
  }

  trackByFilename(index: number, doc: Document): string {
    return doc.name;
  }
}