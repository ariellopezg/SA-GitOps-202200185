{{- define "posts-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "posts-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- include "posts-service.name" . }}
{{- end }}
{{- end }}

{{- define "posts-service.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{ include "posts-service.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "posts-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "posts-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

