{{- define "comments-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "comments-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- include "comments-service.name" . }}
{{- end }}
{{- end }}

{{- define "comments-service.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{ include "comments-service.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "comments-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "comments-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

